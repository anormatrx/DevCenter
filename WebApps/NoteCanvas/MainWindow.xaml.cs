using System.IO;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Threading;
using NoteCanvas.Controls;
using NoteCanvas.Models;
using NoteCanvas.Services;

namespace NoteCanvas;

public partial class MainWindow : Window
{
    private readonly StorageService _storage = new();
    private readonly ReminderService _reminder = new();
    private readonly List<NoteControl> _noteControls = new();
    private bool _isFocusMode;
    private NoteControl? _focusedNote;

    public MainWindow()
    {
        InitializeComponent();
        _reminder.ReminderTriggered += OnReminderTriggered;
        Loaded += async (_, _) => await LoadNotesAsync();
        Closing += async (_, _) =>
        {
            await SaveAllNotesAsync();
            _reminder.Stop();
        };

        var autoSaveTimer = new DispatcherTimer { Interval = TimeSpan.FromMinutes(2) };
        autoSaveTimer.Tick += async (_, _) =>
        {
            if (_noteControls.Count > 0)
                await SaveAllNotesAsync();
        };
        autoSaveTimer.Start();
    }

    private async Task SaveAllNotesAsync()
    {
        foreach (var ctrl in _noteControls)
            ctrl.SaveContent();
        var notes = _noteControls.Select(c => c.NoteData).ToList();
        await _storage.SaveAsync(notes);
        _reminder.SetNotes(notes);
    }

    private async Task LoadNotesAsync()
    {
        var notes = await _storage.LoadAsync();
        foreach (var note in notes)
            AddNoteControl(note, false);
        _reminder.SetNotes(notes.Select(n => n).ToList());
        UpdateStatus();
    }

    private NoteControl AddNoteControl(Note note, bool selectContent = true)
    {
        var ctrl = new NoteControl(note)
        {
            Width = note.Width,
            Height = note.Height
        };

        Canvas.SetLeft(ctrl, note.X);
        Canvas.SetTop(ctrl, note.Y);
        Canvas.SetZIndex(ctrl, note.ZIndex);
        NoteCanvas.Children.Add(ctrl);
        _noteControls.Add(ctrl);

        ctrl.NoteClosed += OnNoteClosed;
        ctrl.NoteSelected += OnNoteSelected;
        ctrl.NoteModified += OnNoteModified;

        if (selectContent)
        {
            ctrl.Loaded += (_, _) => ctrl.FocusContent();
        }

        return ctrl;
    }

    private void NewNoteButton_Click(object sender, RoutedEventArgs e)
    {
        var note = new Note
        {
            X = 50 + (_noteControls.Count * 30 % 500),
            Y = 50 + (_noteControls.Count * 30 % 400),
            ZIndex = _noteControls.Count
        };

        var ctrl = AddNoteControl(note);
        OnNoteModified();
        UpdateStatus();
    }

    private async void SaveButton_Click(object sender, RoutedEventArgs e)
    {
        foreach (var ctrl in _noteControls)
            ctrl.SaveContent();

        var notes = _noteControls.Select(c => c.NoteData).ToList();
        await _storage.SaveAsync(notes);
        _reminder.SetNotes(notes);

        StatusText.Text = $"تم حفظ {notes.Count} ملاحظة";
    }

    private void FocusButton_Click(object sender, RoutedEventArgs e)
    {
        _isFocusMode = !_isFocusMode;
        FocusButton.Content = _isFocusMode ? "🔍 إلغاء التركيز" : "🔍 وضع التركيز";

        if (_isFocusMode)
        {
            if (_focusedNote == null && _noteControls.Count > 0)
                _focusedNote = _noteControls[^1];

            foreach (var ctrl in _noteControls)
                ctrl.Visibility = ctrl == _focusedNote ? Visibility.Visible : Visibility.Collapsed;
        }
        else
        {
            foreach (var ctrl in _noteControls)
                ctrl.Visibility = Visibility.Visible;
            _focusedNote = null;
        }

        UpdateStatus();
    }

    private void OnNoteClosed(NoteControl ctrl)
    {
        var result = MessageBox.Show("هل تريد حذف هذه الملاحظة؟", "تأكيد الحذف",
            MessageBoxButton.YesNo, MessageBoxImage.Question);
        if (result != MessageBoxResult.Yes) return;

        NoteCanvas.Children.Remove(ctrl);
        _noteControls.Remove(ctrl);
        OnNoteModified();
        UpdateStatus();
    }

    private void OnNoteSelected(NoteControl ctrl)
    {
        _focusedNote = ctrl;
    }

    private void OnNoteModified()
    {
        foreach (var nc in _noteControls)
            nc.SaveContent();
        var notes = _noteControls.Select(nc => nc.NoteData).ToList();
        _reminder.SetNotes(notes);
        UpdateStatus();
    }

    private void NoteCanvas_MouseDown(object sender, MouseButtonEventArgs e)
    {
        if (e.OriginalSource == NoteCanvas)
        {
            foreach (var ctrl in _noteControls)
                ctrl.SaveContent();
        }
    }

    private void UpdateStatus()
    {
        int count = _noteControls.Count;
        string mode = _isFocusMode ? " | وضع التركيز نشط" : "";
        StatusText.Text = $"{count} ملاحظة{(count != 1 ? "ات" : "")}{mode}";
    }

    private void OnReminderTriggered(Note note)
    {
        var result = MessageBox.Show(
            $"تذكير: {note.Title}\n\n{nougat(note.Content)}",
            "🔔 تذكير ملاحظة",
            MessageBoxButton.OK,
            MessageBoxImage.Information);

        note.ReminderAt = null;
        OnNoteModified();
    }

    private static string nougat(string rtf)
    {
        try
        {
            var flowDoc = new System.Windows.Documents.FlowDocument();
            var range = new System.Windows.Documents.TextRange(
                flowDoc.ContentStart, flowDoc.ContentEnd);
            using var ms = new System.IO.MemoryStream(
                System.Text.Encoding.UTF8.GetBytes(rtf));
            range.Load(ms, DataFormats.Rtf);
            return range.Text.Length > 100 ? range.Text[..100] + "..." : range.Text;
        }
        catch
        {
            return "محتويات الملاحظة";
        }
    }
}

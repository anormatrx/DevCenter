using System.Windows;
using System.Windows.Threading;
using NoteCanvas.Models;

namespace NoteCanvas.Services;

public class ReminderService
{
    private readonly DispatcherTimer _timer;
    private List<Note> _notes = new();

    public event Action<Note>? ReminderTriggered;

    public ReminderService()
    {
        _timer = new DispatcherTimer { Interval = TimeSpan.FromSeconds(10) };
        _timer.Tick += CheckReminders;
        _timer.Start();
    }

    public void SetNotes(List<Note> notes) => _notes = notes;

    private void CheckReminders(object? sender, EventArgs e)
    {
        var now = DateTime.Now;
        foreach (var note in _notes)
        {
            if (note.ReminderAt.HasValue &&
                note.ReminderAt.Value <= now &&
                note.ReminderAt.Value > now.AddSeconds(-20))
            {
                ReminderTriggered?.Invoke(note);
            }
        }
    }

    public void Stop() => _timer.Stop();
}

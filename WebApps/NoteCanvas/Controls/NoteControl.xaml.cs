using System.IO;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using NoteCanvas.Models;

namespace NoteCanvas.Controls;

public partial class NoteControl : UserControl
{
    public Note NoteData { get; private set; }
    public event Action<NoteControl>? NoteClosed;
    public event Action<NoteControl>? NoteSelected;
    public event Action? NoteModified;

    private bool _isDragging;
    private Point _dragStartPoint;
    private bool _isResizing;
    private Point _resizeStartPoint;
    private Size _resizeStartSize;
    private bool _formatBarVisible = true;

    private static readonly string[] PresetBgColors = new[]
    {
        "#FFFFE0", "#E0FFE0", "#E0F0FF", "#FFE0F0",
        "#FFF0E0", "#F0E0FF", "#FFFFFF", "#F0F0F0",
        "#FFE0E0", "#E0FFFF", "#F5F5DC", "#FFE4E1"
    };

    private static readonly string[] PresetTextColors = new[]
    {
        "#000000", "#8B0000", "#FF0000", "#FF8C00",
        "#006400", "#008000", "#00008B", "#0000FF",
        "#800080", "#808080", "#A0522D", "#2F4F4F"
    };

    public NoteControl(Note note)
    {
        InitializeComponent();
        NoteData = note;
        LoadNoteData();
        SetupFontComboBoxes();
    }

    private void SetupFontComboBoxes()
    {
        string[] fonts = { "Segoe UI", "Arial", "Times New Roman", "Courier New",
                           "Comic Sans MS", "Verdana", "Tahoma", "Calibri",
                           "Georgia", "Trebuchet MS", "Impact", "Consolas" };
        foreach (var f in fonts)
            FontFamilyCombo.Items.Add(f);

        int[] sizes = { 8, 9, 10, 11, 12, 14, 16, 18, 20, 22, 24, 28, 32, 36, 42, 48, 56, 64, 72 };
        foreach (var s in sizes)
            FontSizeCombo.Items.Add(s);
    }

    private static void SelectComboItem(ComboBox combo, string value)
    {
        foreach (var item in combo.Items)
        {
            if (item.ToString() == value)
            {
                combo.SelectedItem = item;
                return;
            }
        }
        combo.Text = value;
    }

    private void LoadNoteData()
    {
        TitleTextBox.Text = NoteData.Title;
        NoteBorder.Background = ParseColor(NoteData.BackgroundColor);

        if (!string.IsNullOrEmpty(NoteData.Content))
        {
            try
            {
                var range = new TextRange(ContentBox.Document.ContentStart, ContentBox.Document.ContentEnd);
                using var ms = new MemoryStream(System.Text.Encoding.UTF8.GetBytes(NoteData.Content));
                range.Load(ms, DataFormats.Rtf);
            }
            catch
            {
                ContentBox.Document = new FlowDocument();
            }
        }

        SelectComboItem(FontFamilyCombo, NoteData.FontFamily);
        SelectComboItem(FontSizeCombo, NoteData.FontSize.ToString("0"));
        BoldButton.IsChecked = NoteData.FontBold;
        ItalicButton.IsChecked = NoteData.FontItalic;
        UnderlineButton.IsChecked = NoteData.FontUnderline;

        var bgBrush = (Border)BgColorButton.Content;
        bgBrush.Background = ParseColor(NoteData.BackgroundColor);

        var textBrush = (TextBlock)TextColorButton.Content;
        textBrush.Foreground = ParseColor(NoteData.TextColor);

        ReminderButton.Content = NoteData.ReminderAt.HasValue ? "🔔⏰" : "🔔";
    }

    private static Brush ParseColor(string hex)
    {
        try
        {
            var color = (Color)ColorConverter.ConvertFromString(hex);
            return new SolidColorBrush(color);
        }
        catch
        {
            return new SolidColorBrush(Colors.LightYellow);
        }
    }

    public void SaveContent()
    {
        NoteData.Title = TitleTextBox.Text;
        var range = new TextRange(ContentBox.Document.ContentStart, ContentBox.Document.ContentEnd);
        using var ms = new MemoryStream();
        range.Save(ms, DataFormats.Rtf);
        NoteData.Content = System.Text.Encoding.UTF8.GetString(ms.ToArray());
        NoteData.ModifiedAt = DateTime.Now;
    }

    public void FocusContent()
    {
        ContentBox.Focus();
        Keyboard.Focus(ContentBox);
    }

    public void BringToFront()
    {
        if (Parent is Canvas canvas)
        {
            int maxZ = 0;
            foreach (var child in canvas.Children)
            {
                if (child is NoteControl nc && nc != this)
                    maxZ = Math.Max(maxZ, nc.NoteData.ZIndex);
            }
            NoteData.ZIndex = maxZ + 1;
            Canvas.SetZIndex(this, NoteData.ZIndex);
        }
    }

    #region Drag

    private void TitleBar_MouseDown(object sender, MouseButtonEventArgs e)
    {
        if (e.ClickCount == 2)
        {
            _formatBarVisible = !_formatBarVisible;
            FormatBar.Visibility = _formatBarVisible ? Visibility.Visible : Visibility.Collapsed;
            e.Handled = true;
            return;
        }

        if (e.ChangedButton == MouseButton.Left)
        {
            _isDragging = true;
            _dragStartPoint = e.GetPosition(Parent as IInputElement);
            TitleBar.CaptureMouse();
            NoteSelected?.Invoke(this);
            BringToFront();
            e.Handled = true;
        }
    }

    private void TitleBar_MouseMove(object sender, MouseEventArgs e)
    {
        if (!_isDragging) return;
        var current = e.GetPosition(Parent as IInputElement);
        double dx = current.X - _dragStartPoint.X;
        double dy = current.Y - _dragStartPoint.Y;
        _dragStartPoint = current;

        NoteData.X += dx;
        NoteData.Y += dy;
        Canvas.SetLeft(this, NoteData.X);
        Canvas.SetTop(this, NoteData.Y);
    }

    private void TitleBar_MouseUp(object sender, MouseButtonEventArgs e)
    {
        if (_isDragging)
        {
            _isDragging = false;
            TitleBar.ReleaseMouseCapture();
            e.Handled = true;
        }
    }

    #endregion

    #region Resize

    private void Resize_MouseDown(object sender, MouseButtonEventArgs e)
    {
        if (e.ClickCount == 2)
        {
            bool isCompact = Width == 200 && Height == 80;
            Width = isCompact ? NoteData.Width : 200;
            Height = isCompact ? NoteData.Height : 80;
            NoteData.Width = Width;
            NoteData.Height = Height;
            e.Handled = true;
            return;
        }

        if (e.ChangedButton == MouseButton.Left)
        {
            _isResizing = true;
            _resizeStartPoint = e.GetPosition(this);
            _resizeStartSize = new Size(ActualWidth, ActualHeight);
            ResizeHandle.CaptureMouse();
            e.Handled = true;
        }
    }

    private void Resize_MouseMove(object sender, MouseEventArgs e)
    {
        if (!_isResizing) return;
        var current = e.GetPosition(this);
        double dw = current.X - _resizeStartPoint.X;
        double dh = current.Y - _resizeStartPoint.Y;

        double newW = Math.Max(180, _resizeStartSize.Width + dw);
        double newH = Math.Max(120, _resizeStartSize.Height + dh);

        Width = newW;
        Height = newH;
        NoteData.Width = newW;
        NoteData.Height = newH;
    }

    private void Resize_MouseUp(object sender, MouseButtonEventArgs e)
    {
        if (_isResizing)
        {
            _isResizing = false;
            ResizeHandle.ReleaseMouseCapture();
            e.Handled = true;
        }
    }

    #endregion

    #region Formatting

    private void FontFamily_Changed(object sender, SelectionChangedEventArgs e)
    {
        if (FontFamilyCombo.SelectedItem is string font)
            ApplyFontProperty(TextElement.FontFamilyProperty, new FontFamily(font));
    }

    private void FontSize_Changed(object sender, SelectionChangedEventArgs e)
    {
        if (FontSizeCombo.SelectedItem is int size)
            ApplyFontProperty(TextElement.FontSizeProperty, (double)size);
    }

    private void Bold_Checked(object sender, RoutedEventArgs e) =>
        ApplyFontProperty(TextElement.FontWeightProperty, FontWeights.Bold);
    private void Bold_Unchecked(object sender, RoutedEventArgs e) =>
        ApplyFontProperty(TextElement.FontWeightProperty, FontWeights.Normal);

    private void Italic_Checked(object sender, RoutedEventArgs e) =>
        ApplyFontProperty(TextElement.FontStyleProperty, FontStyles.Italic);
    private void Italic_Unchecked(object sender, RoutedEventArgs e) =>
        ApplyFontProperty(TextElement.FontStyleProperty, FontStyles.Normal);

    private void Underline_Checked(object sender, RoutedEventArgs e)
    {
        var selection = ContentBox.Selection;
        if (!selection.IsEmpty)
        {
            TextDecorationCollection underline = TextDecorations.Underline;
            selection.ApplyPropertyValue(Inline.TextDecorationsProperty, underline);
        }
    }
    private void Underline_Unchecked(object sender, RoutedEventArgs e)
    {
        var selection = ContentBox.Selection;
        if (!selection.IsEmpty)
            selection.ApplyPropertyValue(Inline.TextDecorationsProperty, null);
    }

    private void ApplyFontProperty(DependencyProperty prop, object value)
    {
        var selection = ContentBox.Selection;
        if (!selection.IsEmpty)
        {
            selection.ApplyPropertyValue(prop, value);
        }
        else
        {
            ContentBox.Selection.Start.InsertTextInRun("");
            ContentBox.Selection.ApplyPropertyValue(prop, value);
        }
    }

    private void Content_SelectionChanged(object sender, RoutedEventArgs e)
    {
        var selection = ContentBox.Selection;
        if (selection.IsEmpty)
        {
            ResetToolbarState();
            return;
        }

        object fontWeight = selection.GetPropertyValue(TextElement.FontWeightProperty);
        object fontStyle = selection.GetPropertyValue(TextElement.FontStyleProperty);
        object fontFamily = selection.GetPropertyValue(TextElement.FontFamilyProperty);
        object fontSize = selection.GetPropertyValue(TextElement.FontSizeProperty);
        object foreground = selection.GetPropertyValue(TextElement.ForegroundProperty);

        if (fontWeight is FontWeight fw)
            BoldButton.IsChecked = fw == FontWeights.Bold;
        if (fontStyle is FontStyle fs)
            ItalicButton.IsChecked = fs == FontStyles.Italic;
        if (fontFamily is FontFamily ff)
            FontFamilyCombo.Text = ff.Source;
        if (fontSize is double fsz)
            FontSizeCombo.Text = fsz.ToString("0.#");
    }

    private void ResetToolbarState()
    {
        BoldButton.IsChecked = NoteData.FontBold;
        ItalicButton.IsChecked = NoteData.FontItalic;
        UnderlineButton.IsChecked = NoteData.FontUnderline;
        FontFamilyCombo.Text = NoteData.FontFamily;
        FontSizeCombo.Text = NoteData.FontSize.ToString();
    }

    #endregion

    #region Colors

    private void TextColorButton_Click(object sender, RoutedEventArgs e)
    {
        var popup = CreateColorPopup(PresetTextColors, color =>
        {
            NoteData.TextColor = color;
            var tb = (TextBlock)TextColorButton.Content;
            tb.Foreground = ParseColor(color);
            var selection = ContentBox.Selection;
            if (!selection.IsEmpty)
                selection.ApplyPropertyValue(TextElement.ForegroundProperty, ParseColor(color));
            else
                ContentBox.Selection.ApplyPropertyValue(TextElement.ForegroundProperty, ParseColor(color));
        });
        popup.PlacementTarget = TextColorButton;
        popup.IsOpen = true;
    }

    private void BgColorButton_Click(object sender, RoutedEventArgs e)
    {
        var popup = CreateColorPopup(PresetBgColors, color =>
        {
            NoteData.BackgroundColor = color;
            NoteBorder.Background = ParseColor(color);
            var bgBrush = (Border)BgColorButton.Content;
            bgBrush.Background = ParseColor(color);
            NoteModified?.Invoke();
        });
        popup.PlacementTarget = BgColorButton;
        popup.IsOpen = true;
    }

    private System.Windows.Controls.Primitives.Popup CreateColorPopup(string[] colors, Action<string> onSelect)
    {
        var popup = new System.Windows.Controls.Primitives.Popup
        {
            StaysOpen = false,
            Placement = System.Windows.Controls.Primitives.PlacementMode.Bottom
        };

        var wrap = new WrapPanel { Width = 150, Background = Brushes.White };
        var border = new Border
        {
            Child = wrap,
            BorderBrush = Brushes.Gray,
            BorderThickness = new Thickness(1),
            CornerRadius = new CornerRadius(4),
            Background = Brushes.White,
            Padding = new Thickness(4)
        };
        popup.Child = border;

        foreach (var hex in colors)
        {
            var color = ParseColor(hex);
            var btn = new Button
            {
                Width = 24,
                Height = 24,
                Margin = new Thickness(2),
                Background = color,
                BorderBrush = Brushes.Gray,
                BorderThickness = new Thickness(1),
                Tag = hex
            };
            btn.Click += (_, _) =>
            {
                onSelect((string)btn.Tag);
                popup.IsOpen = false;
            };
            wrap.Children.Add(btn);
        }

        return popup;
    }

    #endregion

    #region Reminder

    private void ReminderButton_Click(object sender, RoutedEventArgs e)
    {
        var dialog = new ReminderDialog { Owner = Application.Current.MainWindow };
        if (NoteData.ReminderAt.HasValue)
            dialog.SetReminder(NoteData.ReminderAt.Value);
        if (dialog.ShowDialog() == true)
        {
            NoteData.ReminderAt = dialog.GetReminder();
            ReminderButton.Content = NoteData.ReminderAt.HasValue ? "🔔⏰" : "🔔";
            NoteModified?.Invoke();
        }
    }

    #endregion

    #region Events

    private void CloseButton_Click(object sender, RoutedEventArgs e)
    {
        NoteClosed?.Invoke(this);
    }

    private void Content_PreviewMouseDown(object sender, MouseButtonEventArgs e)
    {
        NoteSelected?.Invoke(this);
        BringToFront();
    }

    private void Title_TextChanged(object sender, TextChangedEventArgs e)
    {
        NoteData.Title = TitleTextBox.Text;
        NoteModified?.Invoke();
    }

    #endregion
}

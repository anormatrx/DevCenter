namespace NoteCanvas.Models;

public class Note
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public string Title { get; set; } = "ملاحظة جديدة";
    public string Content { get; set; } = "";
    public double X { get; set; } = 100;
    public double Y { get; set; } = 100;
    public double Width { get; set; } = 300;
    public double Height { get; set; } = 320;
    public string BackgroundColor { get; set; } = "#FFFFE0";
    public string TextColor { get; set; } = "#000000";
    public string FontFamily { get; set; } = "Segoe UI";
    public double FontSize { get; set; } = 14;
    public bool FontBold { get; set; }
    public bool FontItalic { get; set; }
    public bool FontUnderline { get; set; }
    public DateTime CreatedAt { get; set; } = DateTime.Now;
    public DateTime ModifiedAt { get; set; } = DateTime.Now;
    public DateTime? ReminderAt { get; set; }
    public int ZIndex { get; set; }
}

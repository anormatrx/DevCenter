using System.Globalization;
using System.Windows;

namespace NoteCanvas.Controls;

public partial class ReminderDialog : Window
{
    private DateTime? _reminder;

    public ReminderDialog()
    {
        InitializeComponent();
        DatePicker.SelectedDate = DateTime.Today;
        TimeTextBox.Text = DateTime.Now.AddHours(1).ToString("HH:mm");
    }

    public void SetReminder(DateTime dt)
    {
        DatePicker.SelectedDate = dt.Date;
        TimeTextBox.Text = dt.ToString("HH:mm");
    }

    public DateTime? GetReminder() => _reminder;

    private void Ok_Click(object sender, RoutedEventArgs e)
    {
        if (DatePicker.SelectedDate is DateTime date &&
            TimeSpan.TryParseExact(TimeTextBox.Text, @"hh\:mm", CultureInfo.InvariantCulture, out var time))
        {
            _reminder = date.Date + time;
            DialogResult = true;
        }
        else
        {
            MessageBox.Show("الرجاء إدخال تاريخ ووقت صحيحين", "خطأ", MessageBoxButton.OK, MessageBoxImage.Warning);
        }
    }

    private void Cancel_Click(object sender, RoutedEventArgs e)
    {
        DialogResult = false;
    }
}

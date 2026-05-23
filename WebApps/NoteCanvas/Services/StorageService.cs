using System.IO;
using System.Text.Json;
using NoteCanvas.Models;

namespace NoteCanvas.Services;

public class StorageService
{
    private readonly string _filePath;

    public StorageService()
    {
        string appData = Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
            "NoteCanvas");
        Directory.CreateDirectory(appData);
        _filePath = Path.Combine(appData, "notes.json");
    }

    public async Task<List<Note>> LoadAsync()
    {
        if (!File.Exists(_filePath))
            return new List<Note>();

        try
        {
            string json = await File.ReadAllTextAsync(_filePath);
            return JsonSerializer.Deserialize<List<Note>>(json) ?? new List<Note>();
        }
        catch
        {
            return new List<Note>();
        }
    }

    public async Task SaveAsync(List<Note> notes)
    {
        var options = new JsonSerializerOptions { WriteIndented = true };
        string json = JsonSerializer.Serialize(notes, options);
        await File.WriteAllTextAsync(_filePath, json);
    }
}

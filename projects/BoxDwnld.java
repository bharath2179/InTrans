using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using Box.V2.Config;
using Box.V2.JWTAuth;

namespace BoxDownloadAllFiles {
  class Program {
    static void Main (string[] args) {
      ExecuteMainAsync ().Wait ();
    }

    private static async Task ExecuteMainAsync () {
      using (FileStream fs = new FileStream ($"./config.json", FileMode.Open)) {
        var session = new BoxJWTAuth (BoxConfig.CreateFromJsonFile (fs));
        var client = session.AdminClient (session.AdminToken ());
        var folderId = "987654321";
        var folder = await client.FoldersManager.GetInformationAsync (folderId);
        var folderName = folder.Name;
        var localFolderPath = Path.Combine (Directory.GetCurrentDirectory (), folderName);
        ResetLocalFolder (localFolderPath);

        var items = await client.FoldersManager.GetFolderItemsAsync (folderId, 1000, autoPaginate : true);
        var fileDownloadTasks = new List<Task> ();
        var files = items.Entries.Where (i => i.Type == "file");
        foreach (var file in files) {
          fileDownloadTasks.Add (client.FilesManager.DownloadStreamAsync (file.Id).ContinueWith ((t) => {
            var localFile = File.Create (Path.Combine (localFolderPath, file.Name));
            return t.Result.CopyToAsync (localFile);
          }));
        }
        await Task.WhenAll (fileDownloadTasks);
      }
    }

    private static void ResetLocalFolder (string localFolderPath) {
      if (!Directory.Exists (localFolderPath)) {
        Directory.CreateDirectory (localFolderPath);
      } else {
        foreach (var file in Directory.EnumerateFiles (localFolderPath)) {
          File.Delete (Path.Combine (localFolderPath, file));
        }
        Directory.Delete (localFolderPath);
        Directory.CreateDirectory (localFolderPath);
      }
    }
  }
}
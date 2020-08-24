import com.box.sdk.BoxConfig;
import com.box.sdk.BoxDeveloperEditionAPIConnection;
import com.box.sdk.BoxFile;
import com.box.sdk.BoxFolder;
import com.box.sdk.BoxItem;
import java.io.BufferedReader;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class Playground {

 public static void main(String[] args) throws Exception {
  Path configPath = Paths.get("config.json");
  Path currentDir = Paths.get("").toAbsolutePath();
  try (BufferedReader reader = Files.newBufferedReader(configPath, Charset.forName("UTF-8"))) {
   BoxConfig boxConfig = BoxConfig.readFrom(reader);
   BoxDeveloperEditionAPIConnection client = BoxDeveloperEditionAPIConnection.getAppEnterpriseConnection(boxConfig);
   String folderId = "121098032966";
   BoxFolder folder = new BoxFolder(client, folderId);
   String folderName = folder.getInfo().getName();
   Path localFolderPath = currentDir.resolve(Paths.get(folderName));
   if (!Files.exists(localFolderPath)) {
    localFolderPath = Files.createDirectory(localFolderPath);
   } else {
    localFolderPath = resetLocalFolder(localFolderPath);
   }

   for (BoxItem.Info itemInfo: folder) {
    if (itemInfo instanceof BoxFile.Info) {
     BoxFile.Info fileInfo = (BoxFile.Info) itemInfo;
     BoxFile file = new BoxFile(client, fileInfo.getID());
     String localFilePath = localFolderPath.resolve(Paths.get(fileInfo.getName())).toAbsolutePath().toString();
     FileOutputStream stream = new FileOutputStream(localFilePath);
     file.download(stream);
     stream.close();
    }
   }

  }
 }

 static Path resetLocalFolder(Path localFolderPath) throws IOException {
  Files.list(localFolderPath).forEach(file -> {
   System.out.println(file.getFileName());
   try {
    Files.delete(file.toAbsolutePath());
   } catch (IOException e) {}
  });
  Files.delete(localFolderPath);
  localFolderPath = Files.createDirectory(localFolderPath);
  return localFolderPath;
 }
}
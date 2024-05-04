using System;
using System.Linq;
using System.Threading.Tasks;
using System.Net.Http;
using System.Net;
using System.IO;
using System.IO.Compression;
using System.Diagnostics;

namespace GLMUpdater
{
	static class Utils
	{
		public static async Task<string> GetLatest()
		{
			using (HttpClient httpClient = new HttpClient())
			{
				HttpResponseMessage response = await httpClient.GetAsync("https://github.com/BlueAmulet/GreenLuma-2024-Manager/releases/latest");
				string[] header = response.RequestMessage.RequestUri.Segments;
				return header.Last().Substring(1);
			}
		}

		public static Task DownloadAndExtractFile(string URL)
		{
			using (WebClient client = new WebClient())
			{
				client.Proxy = null;
				client.DownloadFileCompleted += CompletedHandler;
				client.DownloadProgressChanged += ProgressHandler;
				return client.DownloadFileTaskAsync(new Uri(URL), "Release.zip");
			}
		}

		private static void ProgressHandler(object sender, DownloadProgressChangedEventArgs e)
		{
			Console.Write(string.Format("{0}%\r", e.ProgressPercentage.ToString()));
		}

		private static void CompletedHandler(object sender, System.ComponentModel.AsyncCompletedEventArgs e)
		{
			ExtractFile("./Release.zip");
			Process.Start("GreenLuma 2020 Manager.exe", "-NoUpdate -PostUpdate");
		}

		public static void ExtractFile(string path)
		{
			Console.WriteLine("Extracting File...");
			using (ZipArchive archive = ZipFile.OpenRead(path))
			{
				foreach (ZipArchiveEntry entry in archive.Entries)
				{
					string fileName = entry.FullName.Split('/')[1];
					if (fileName != "")
					{
						Console.WriteLine(Path.Combine("./", fileName));
						try
						{
							entry.ExtractToFile(Path.Combine("./", fileName), true);
						}
						catch (Exception)
						{
							entry.ExtractToFile(Path.Combine("./", "new_" + fileName), true);
						}
					}
				}
			}

			Console.WriteLine("Deleting Temporary Files...");
			File.Delete(path);
		}

		public static StreamWriter CreateLogger()
		{
			FileStream logOutput = new FileStream("UpdaterLog.txt", FileMode.Create);
			StreamWriter logWriter = new StreamWriter(logOutput);
			logWriter.AutoFlush = true;

			return logWriter;
		}
	}
}

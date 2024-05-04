using System;
using System.Threading.Tasks;
using System.IO;
using System.Net;
using System.Diagnostics;
using Newtonsoft.Json.Linq;

namespace GLMUpdater
{
	class Updater
	{
		private readonly string dataPath = Environment.ExpandEnvironmentVariables("%localappdata%/GLR_Manager/");
		private readonly string downloadURL = "https://github.com/BlueAmulet/GreenLuma-2024-Manager/releases/download/v{0}/GreenLuma.2020.Manager.zip";
		private string latestVersionString;
		private string currentVersionString;
		private readonly StreamWriter logger = Utils.CreateLogger();
		public async Task IsUpdated()
		{
			try
			{
				latestVersionString = await Utils.GetLatest();
			}
			catch (Exception e)
			{
				PrintError(e.StackTrace, "Error while trying to get the last version.");
				return;
			}

			try
			{
				string configJSON = File.ReadAllText(dataPath + "config.json");
				currentVersionString = (string)JObject.Parse(configJSON)["version"];
			}
			catch (Exception)
			{
				return;
			}

			Version currentVersion = new Version(currentVersionString);
			Version latestVersion = new Version(latestVersionString);

			if (currentVersion.CompareTo(latestVersion) < 0)
			{
				Console.WriteLine("Outdated");

				foreach (Process process in Process.GetProcessesByName("GreenLuma 2020 Manager"))
				{
					if (!process.HasExited)
					{
						process.Kill();
					}
				}

				while (Process.GetProcessesByName("GreenLuma 2020 Manager").Length > 0)
				{
					System.Threading.Thread.Sleep(500);
				}

				try
				{
					Console.WriteLine("Downloading Latest Version...");
					await Utils.DownloadAndExtractFile(string.Format(downloadURL, latestVersionString));
				}
				catch (WebException e)
				{
					PrintError(e.StackTrace, "Error while downloading.");
				}
				catch (Exception e)
				{
					PrintError(e.StackTrace, "Error while extracting.");
				}
			}
			else
			{
				Console.WriteLine("The Program is Up to date");
			}
		}

		private void PrintError(string stack, string mesage)
		{
			Console.WriteLine(mesage);
			logger.WriteLine(stack);

			Console.WriteLine("Press any key to close...");
			Console.ReadLine();
		}
	}

}

namespace GLMUpdater
{
	static class Program
	{
		static void Main(string[] args)
		{
			Updater updater = new Updater();
			updater.IsUpdated().Wait();
		}
	}
}

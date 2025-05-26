using System;
using System.Windows.Forms;

namespace CSharpCompilerTool
{
    static class Program
    {
        // The main entry point for the application
        [STAThread]
        static void Main()
        {
            // Enables visual styles and makes the application use the appropriate rendering mode for controls
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);

            // Run the main form of the application
            Application.Run(new MainForm());
        }
    }
}

using System;
using System.Diagnostics;
using System.IO;
using System.Windows.Forms;

namespace CSharpCompilerTool
{
    public partial class MainForm : Form
    {
        public MainForm()
        {
            InitializeComponent();
        }

        private void compileButton_Click(object sender, EventArgs e)
        {
            string basePath = clBasePathTextBox.Text.Trim();
            string options = compilerOptionsTextBox.Text.Trim();
            string sourceCode = cppSourceCodeTextBox.Text;

            // Check if the base path is valid
            if (string.IsNullOrWhiteSpace(basePath) || !Directory.Exists(basePath))
            {
                MessageBox.Show("Invalid CL Base Path.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            // Check if the C++ source code is provided
            if (string.IsNullOrWhiteSpace(sourceCode))
            {
                MessageBox.Show("C++ Source Code is empty.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            // Save C++ code to a temporary .cpp file
            string tempCppPath = Path.Combine(Path.GetTempPath(), "test.cpp");
            try
            {
                File.WriteAllText(tempCppPath, sourceCode);
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Failed to write temporary file: {ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            // Define configurations and corresponding output text boxes
            string[] configs = { "amd64chk", "amd64ret", "x86chk", "x86ret" };
            TextBox[] outputBoxes = { amd64chkTextBox, amd64retTextBox, x86chkTextBox, x86retTextBox };

            // Visual Studio Command Prompt Path (Hardcoded)
            string vsVarsBatchPath = @"C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Auxiliary\Build\vcvarsall.bat";

            // Default compiler options if none provided
            if (string.IsNullOrEmpty(options))
            {
                options = "/c /EHsc"; // Default options: Compile only and enable exception handling
            }

            // Loop over each configuration
            for (int i = 0; i < configs.Length; i++)
            {
                string config = configs[i];
                string platform = config.StartsWith("amd64") ? "amd64" : "x86";
                string flavor = config.Contains("chk") ? $"{platform}chk" : $"{platform}ret";

                // Construct the full path for cl.exe
                string clExePath;
                if (platform == "amd64")
                {
                    clExePath = Path.Combine(basePath, $"binaries.{flavor}", "bin", "amd64", "cl.exe");
                }
                else
                {
                    // Correct the path for x86 configuration
                    clExePath = Path.Combine(basePath, $"binaries.{flavor}", "bin", "i386", "cl.exe"); // Fix for x86 path
                }

                // -I path for include directory
                string includePath = Path.Combine(basePath, $"binaries.{flavor}", "inc");

                // Construct the command line arguments
                string arguments = $"-I\"{includePath}\" {options} \"{tempCppPath}\"";
                string commandLine = $"\"{clExePath}\" {arguments}";

                // Check if vcvarsall.bat exists
                if (!File.Exists(vsVarsBatchPath))
                {
                    outputBoxes[i].Text = $"[Command]: {commandLine}\r\n\r\n[Output]:\r\nvcvarsall.bat not found!";
                    continue;
                }

                // Execute the compilation in the corresponding Visual Studio developer command prompt
                string output;
                try
                {
                    var process = new Process();
                    process.StartInfo.FileName = "cmd.exe";

                    // Adjust platform to x86 or amd64 based on the current configuration
                    string platformArgument = platform == "amd64" ? "amd64" : "x86"; // Fix for x86 platform argument

                    // Construct the full command
                    process.StartInfo.Arguments = $"/C \"\"{vsVarsBatchPath}\" {platformArgument} && \"{clExePath}\" {arguments}\"";

                    process.StartInfo.RedirectStandardOutput = true;
                    process.StartInfo.RedirectStandardError = true;
                    process.StartInfo.UseShellExecute = false;
                    process.StartInfo.CreateNoWindow = true;

                    process.Start();

                    // Read both standard output and error output
                    string stdout = process.StandardOutput.ReadToEnd();
                    string stderr = process.StandardError.ReadToEnd();
                    process.WaitForExit();

                    // Format the result
                    output = $"[Command]: {commandLine}\r\n\r\n[Compiler Options]: {options}\r\n\r\n[Output]:\r\n{stdout}{stderr}";
                }
                catch (Exception ex)
                {
                    output = $"[Command]: {commandLine}\r\n\r\n[Compiler Options]: {options}\r\n\r\n[Output]:\r\nFailed to execute: {ex.Message}";
                }

                // Display the result in the appropriate output box
                outputBoxes[i].Text = output;
            }
        }
    }
}

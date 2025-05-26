using System;
using System.Drawing;
using System.Windows.Forms;

namespace CSharpCompilerTool
{
    partial class MainForm
    {
        private System.ComponentModel.IContainer components = null;

        private Label clBasePathLabel;
        private TextBox clBasePathTextBox;
        private Label compilerOptionsLabel;
        private TextBox compilerOptionsTextBox;
        private Label cppSourceCodeLabel;
        private TextBox cppSourceCodeTextBox;
        private Button compileButton;

        private Label amd64chkLabel;
        private Label amd64retLabel;
        private Label x86chkLabel;
        private Label x86retLabel;

        private TextBox amd64chkTextBox;
        private TextBox amd64retTextBox;
        private TextBox x86chkTextBox;
        private TextBox x86retTextBox;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        /// <summary>
        /// Initialize all UI components and layout
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            this.clBasePathLabel = new Label();
            this.clBasePathTextBox = new TextBox();
            this.compilerOptionsLabel = new Label();
            this.compilerOptionsTextBox = new TextBox();
            this.cppSourceCodeLabel = new Label();
            this.cppSourceCodeTextBox = new TextBox();
            this.compileButton = new Button();

            this.amd64chkLabel = new Label();
            this.amd64retLabel = new Label();
            this.x86chkLabel = new Label();
            this.x86retLabel = new Label();

            this.amd64chkTextBox = new TextBox();
            this.amd64retTextBox = new TextBox();
            this.x86chkTextBox = new TextBox();
            this.x86retTextBox = new TextBox();

            this.SuspendLayout();

            // Layout settings
            int formWidth = 1680;
            int formHeight = 500*4;
            int leftColWidth = 560;
            int outputColWidth = (formWidth - leftColWidth) / 2;
            int controlHeight = 20;
            int margin = 10;
            int labelHeight = 15;

            // === First Column ===

            // Get latest CL Path
            var directories = Directory.GetDirectories(@"xxx");
            string latestVersionPath = directories
                .OrderByDescending(d => d)
                .FirstOrDefault();

            // CL Base Path Label
            clBasePathLabel.Text = "CL Base Path:";
            clBasePathLabel.Location = new Point(margin, margin);
            clBasePathLabel.Size = new Size(leftColWidth - 2 * margin, labelHeight);

            // CL Base Path TextBox
            clBasePathTextBox.Location = new Point(margin, clBasePathLabel.Bottom + 2);
            clBasePathTextBox.Size = new Size(leftColWidth - 2 * margin, controlHeight);
            clBasePathTextBox.Text = latestVersionPath;

            // Compiler Options Label
            compilerOptionsLabel.Text = "Compiler Options:";
            compilerOptionsLabel.Location = new Point(margin, clBasePathTextBox.Bottom + margin);
            compilerOptionsLabel.Size = new Size(leftColWidth - 2 * margin, labelHeight);

            // Compiler Options TextBox
            compilerOptionsTextBox.Location = new Point(margin, compilerOptionsLabel.Bottom + 2);
            compilerOptionsTextBox.Size = new Size(leftColWidth - 2 * margin, controlHeight);
            compilerOptionsTextBox.Text = "/c /EHsc";  // Default options

            // Compile Button
            compileButton.Text = "Compile";
            compileButton.Location = new Point(margin, compilerOptionsTextBox.Bottom + margin);
            compileButton.Size = new Size(leftColWidth - 2 * margin, 30);
            compileButton.Click += new EventHandler(this.compileButton_Click);

            // C++ Source Code Label
            cppSourceCodeLabel.Text = "C++ Source Code:";
            cppSourceCodeLabel.Location = new Point(margin, compileButton.Bottom + margin);
            cppSourceCodeLabel.Size = new Size(leftColWidth - 2 * margin, labelHeight);

            // C++ Source Code TextBox
            cppSourceCodeTextBox.Location = new Point(margin, cppSourceCodeLabel.Bottom + 2);
            cppSourceCodeTextBox.Size = new Size(leftColWidth - 2 * margin, 350*2);
            cppSourceCodeTextBox.Multiline = true;
            cppSourceCodeTextBox.ScrollBars = ScrollBars.Vertical;

            // === Output Area (Right Columns) ===
            int outputTop = clBasePathLabel.Top;
            int outputHeight = cppSourceCodeTextBox.Bottom - outputTop;
            int eachOutputHeight = (outputHeight - margin) / 2;

            // First row labels
            amd64chkLabel.Text = "Result amd64chk";
            amd64chkLabel.Location = new Point(leftColWidth + margin, outputTop);
            amd64chkLabel.Size = new Size(outputColWidth - 2 * margin, labelHeight);

            amd64retLabel.Text = "Result amd64ret";
            amd64retLabel.Location = new Point(leftColWidth + outputColWidth + margin, outputTop);
            amd64retLabel.Size = new Size(outputColWidth - 2 * margin, labelHeight);

            // First row TextBoxes
            int outputBoxTop1 = amd64chkLabel.Bottom + 2;
            int outputBoxHeight = eachOutputHeight - labelHeight - 2;

            amd64chkTextBox.Location = new Point(leftColWidth + margin, outputBoxTop1);
            amd64chkTextBox.Size = new Size(outputColWidth - 2 * margin, outputBoxHeight);
            amd64chkTextBox.Multiline = true;
            amd64chkTextBox.ScrollBars = ScrollBars.Vertical;

            amd64retTextBox.Location = new Point(leftColWidth + outputColWidth + margin, outputBoxTop1);
            amd64retTextBox.Size = new Size(outputColWidth - 2 * margin, outputBoxHeight);
            amd64retTextBox.Multiline = true;
            amd64retTextBox.ScrollBars = ScrollBars.Vertical;

            // Second row labels
            int outputBoxTop2 = outputBoxTop1 + outputBoxHeight + margin;
            x86chkLabel.Text = "Result x86chk";
            x86chkLabel.Location = new Point(leftColWidth + margin, outputBoxTop2);
            x86chkLabel.Size = new Size(outputColWidth - 2 * margin, labelHeight);

            x86retLabel.Text = "Result x86ret";
            x86retLabel.Location = new Point(leftColWidth + outputColWidth + margin, outputBoxTop2);
            x86retLabel.Size = new Size(outputColWidth - 2 * margin, labelHeight);

            // Second row TextBoxes
            int outputBoxTop3 = x86chkLabel.Bottom + 2;
            x86chkTextBox.Location = new Point(leftColWidth + margin, outputBoxTop3);
            x86chkTextBox.Size = new Size(outputColWidth - 2 * margin, outputBoxHeight);
            x86chkTextBox.Multiline = true;
            x86chkTextBox.ScrollBars = ScrollBars.Vertical;

            x86retTextBox.Location = new Point(leftColWidth + outputColWidth + margin, outputBoxTop3);
            x86retTextBox.Size = new Size(outputColWidth - 2 * margin, outputBoxHeight);
            x86retTextBox.Multiline = true;
            x86retTextBox.ScrollBars = ScrollBars.Vertical;


            // === Add Controls ===
            this.Controls.Add(clBasePathLabel);
            this.Controls.Add(clBasePathTextBox);
            this.Controls.Add(compilerOptionsLabel);
            this.Controls.Add(compilerOptionsTextBox);
            this.Controls.Add(compileButton);
            this.Controls.Add(cppSourceCodeLabel);
            this.Controls.Add(cppSourceCodeTextBox);

            this.Controls.Add(amd64chkLabel);
            this.Controls.Add(amd64chkTextBox);
            this.Controls.Add(amd64retLabel);
            this.Controls.Add(amd64retTextBox);
            this.Controls.Add(x86chkLabel);
            this.Controls.Add(x86chkTextBox);
            this.Controls.Add(x86retLabel);
            this.Controls.Add(x86retTextBox);

            // === Main Form Settings ===
            this.ClientSize = new Size(formWidth, formHeight);
            this.Name = "MainForm";
            this.Text = "C++ Multi-Config Compiler Tool";
            this.ResumeLayout(false);
            this.PerformLayout();
        }
    }
}

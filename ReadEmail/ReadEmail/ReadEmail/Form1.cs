using Google.Apis.Auth.OAuth2;
using Google.Apis.Gmail.v1;
using Google.Apis.Gmail.v1.Data;
using Google.Apis.Services;
using Google.Apis.Util.Store;
using System;
using System.Collections.Generic;
using System.Data;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace ReadEmail
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }
        String emailPlainText = "";
        string[] Scopes = {
            GmailService.Scope.GmailReadonly
        };
        GmailService service;
        string myEmail = "vanhieu2910@gmail.com";
        string ApplicationName = "Gmail API .NET Quickstart";
        private void button1_Click(object sender, EventArgs e)
        {

            UserCredential credential;
            using (var stream = new FileStream("client_secret.json", FileMode.Open, FileAccess.Read))
            {
                string credPath = System.IO.Directory.GetCurrentDirectory();
                credPath = Path.Combine(credPath, ".credentials");
                credential = GoogleWebAuthorizationBroker.AuthorizeAsync(GoogleClientSecrets.Load(stream).Secrets, Scopes, "user", CancellationToken.None, new FileDataStore(credPath, true)).Result;
            }
            // Create Gmail API service.   
            service = new GmailService(new BaseClientService.Initializer()
            {
                HttpClientInitializer = credential,
                ApplicationName = ApplicationName,
            });
            var inboxlistRequest = service.Users.Messages.List(myEmail);
            inboxlistRequest.LabelIds = "INBOX";

            inboxlistRequest.IncludeSpamTrash = false;
            //get our emails   
            var emailListResponse = inboxlistRequest.Execute();
            if (emailListResponse != null && emailListResponse.Messages != null)
            {
                //loop through each email and get what fields you want...   
                foreach (var email in emailListResponse.Messages)
                {
                    var emailInfoRequest = service.Users.Messages.Get(myEmail, email.Id);
                    var emailInfoResponse = emailInfoRequest.Execute();
                    if (emailInfoResponse != null)
                    {
                        String from = "";
                        String date = "";
                        String subject = "";
                        //loop through the headers to get from,date,subject, body  
                        foreach (var mParts in emailInfoResponse.Payload.Headers)
                        {
                            if (mParts.Name == "Date")
                            {
                                date = mParts.Value;
                            }
                            else if (mParts.Name == "From")
                            {
                                from = mParts.Value;
                            }
                            else if (mParts.Name == "Subject")
                            {
                                subject = mParts.Value;
                            }
                        }
                        table.Rows.Add(email.Id, from, subject, date);
                    }
                }
                dataGridView1.DataSource = table;
            }
        }



        public static byte[] FromBase64ForUrlString(string base64ForUrlInput)
        {
            int padChars = (base64ForUrlInput.Length % 4) == 0 ? 0 : (4 - (base64ForUrlInput.Length % 4));
            StringBuilder result = new StringBuilder(base64ForUrlInput, base64ForUrlInput.Length + padChars);
            result.Append(String.Empty.PadRight(padChars, '='));
            result.Replace('-', '+');
            result.Replace('_', '/');
            return Convert.FromBase64String(result.ToString());
        }
        DataTable table;

        private void Form1_Load(object sender, EventArgs e)
        {
            table = new DataTable();
            table.Columns.Add("EmailID", typeof(string));
            table.Columns.Add("From", typeof(string));
            table.Columns.Add("Subject", typeof(string));
            table.Columns.Add("Date", typeof(string));
        }

        public string GetContentByEmailID(string EmailID, bool isPlain)
        {
            try
            {
                var emailInfoRequest = service.Users.Messages.Get(myEmail, EmailID);
                var emailInfoResponse = emailInfoRequest.Execute();
                if (emailInfoResponse != null)
                {
                    String from = "";
                    String date = "";
                    String subject = "";
                    //loop through the headers to get from,date,subject, body  
                    foreach (var mParts in emailInfoResponse.Payload.Headers)
                    {
                        if (mParts.Name == "Date")
                        {
                            date = mParts.Value;
                        }
                        else if (mParts.Name == "From")
                        {
                            from = mParts.Value;
                        }
                        else if (mParts.Name == "Subject")
                        {
                            subject = mParts.Value;
                        }
                        if (date != "" && from != "")
                        {
                            string decodedString = "";
                            if (emailInfoResponse.Payload.Parts == null)
                            {
                                emailPlainText = emailInfoResponse.Snippet;
                            }
                            else
                            {
                                foreach (MessagePart p in emailInfoResponse.Payload.Parts)
                                {
                                    if (p.MimeType == "text/html" && !isPlain)
                                    {
                                        byte[] data = FromBase64ForUrlString(p.Body.Data);
                                        decodedString = Encoding.UTF8.GetString(data);
                                    }else if (p.MimeType == "text/plain")
                                    {
                                        byte[] data = FromBase64ForUrlString(p.Body.Data);
                                        emailPlainText = Encoding.UTF8.GetString(data);
                                    }
                                }
                            }
                            if(decodedString != "")
                            {
                                return decodedString;
                            }
                            return emailPlainText;
                        }
                    }
                }
            }
            catch
            {

            }
            return "";

        }

        private async void btnKiemtra_ClickAsync(object sender, EventArgs e)
        {
            var paras = new Dictionary<string, string>();
            paras.Add("email", emailPlainText);
            var res = await Request.PostRequestAsync("http://localhost:1234/check", paras);
            MessageBox.Show(res.ToString());
        }

        private void Cell_Double_Click(object sender, DataGridViewCellEventArgs e)
        {
            if (dataGridView1.SelectedCells.Count > 0)
            {
                int selectedrowindex = dataGridView1.SelectedCells[0].RowIndex;

                DataGridViewRow selectedRow = dataGridView1.Rows[selectedrowindex];

                string email_id = Convert.ToString(selectedRow.Cells["EmailID"].Value);

                string bodyEmail = GetContentByEmailID(email_id, ckPlainText.Checked);
                webBrowser1.DocumentText = bodyEmail;

            }
        }
    }
}

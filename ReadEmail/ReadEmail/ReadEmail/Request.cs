using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;


namespace ReadEmail
{
    public class Request
    {
        private static HttpClient client = new HttpClient();


        public static async Task<string> PostRequestAsync(String url, Dictionary<string, string> paras)
        {

            var content = new FormUrlEncodedContent(paras);

            var response = await client.PostAsync(url, content);


            if (response.IsSuccessStatusCode)
            {
                var responseString = await response.Content.ReadAsStringAsync();

                return responseString;
            }
            else
            {
                return "Error Code" +
                response.StatusCode + " : Message - " + response.ReasonPhrase;
            }
        }

        public static async Task<string> GetRequestAsync(String url)
        {
            var responseString = await client.GetStringAsync(url);
            return responseString;
        }
    }
}

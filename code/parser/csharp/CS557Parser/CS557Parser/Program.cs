using HtmlAgilityPack;
using NDesk.Options;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Web;
using System.Xml;
using System.Xml.Linq;

namespace CS557Parser
{
    class Program
    {
        static void Main(string[] args)
        {
            //   string decoded = HttpUtility.HtmlDecode(html);
            string outputFile = null;
            string inputFile = null;
            string type = null;

            var p = new OptionSet() {
                { "output=", v => outputFile = v },
   	            { "input=", v => inputFile = v },
                { "type=", v => type= v }
            };

            List<string> extra = p.Parse(args);

            if (string.Equals(type, "posts", StringComparison.OrdinalIgnoreCase))
            {
                ParsePostsFile(inputFile, outputFile);
            }
            else if (string.Equals(type, "answers", StringComparison.OrdinalIgnoreCase))
            {
                ParseAnswersFile(inputFile, outputFile);
            }
        }

        private static void ParseAnswersFile(string inputFile, string outputFile)
        {
            List<int> questionIds = new List<int>(); /* List of all questions tagged c or c++ */
            bool writeComma = false;

            using (StreamWriter outFile = new StreamWriter(outputFile))
            {
                outFile.WriteLine("LOCK TABLES `answer` WRITE;");
                outFile.Write("INSERT INTO `answer`");
                outFile.Write("(answerId,parentId,creationDate,score,code,ownerUserId,lastEditorUserId,lastEditorDisplayName,lastEditDate,lastActivityDate,commentCount,communityOwnedDate)");
                outFile.WriteLine(" VALUES ");

                using (FileStream fsSource = new FileStream(inputFile, FileMode.Open, FileAccess.Read))
                {
                    using (XmlReader reader = XmlReader.Create(fsSource))
                    {
                        reader.ReadToDescendant("posts");
                        reader.ReadToDescendant("row");

                        do
                        {
                            if (writeComma) outFile.WriteLine(",");
                            writeComma = ParseAnswer(questionIds, outFile, reader);
                        } while (reader.ReadToNextSibling("row"));
                    }
                }

                outFile.WriteLine(";");
                outFile.WriteLine("UNLOCK TABLES;");
            }
        }

        private static void ParsePostsFile(string inputFile, string outputFile)
        {
            bool writeComma = false;

            using (StreamWriter outFile = new StreamWriter(outputFile))
            {
                outFile.WriteLine("LOCK TABLES `question` WRITE;");
                outFile.Write("INSERT INTO `question`");
                outFile.Write("(postId,tags,acceptedAnswerId,creationDate,score,viewCount,ownerUserId,lastEditorUserId,lastEditorDisplayName,lastEditDate,lastActivityDate,title,answerCount,commentCount,favoriteCount,communityOwnedDate,body)");
                outFile.WriteLine(" VALUES ");

                using (FileStream fsSource = new FileStream(inputFile, FileMode.Open, FileAccess.Read))
                {
                    using (XmlReader reader = XmlReader.Create(fsSource))
                    {
                        reader.ReadToDescendant("posts");
                        reader.ReadToDescendant("row");

                        do
                        {
                            if (writeComma) outFile.WriteLine(",");
                            writeComma = ParsePost(outFile, reader);
                        } while (reader.ReadToNextSibling("row"));
                    }
                }

                outFile.WriteLine(";");
                outFile.WriteLine("UNLOCK TABLES;");
            }
        }

        private static bool ParseAnswer(List<int> questionIds, StreamWriter outFile, XmlReader reader)
        {
            string postTypeId = reader.GetAttribute("PostTypeId");
            string id = reader.GetAttribute("Id");

            if ("1" == postTypeId)
            {
                string tags = HttpUtility.HtmlDecode(reader.GetAttribute("Tags"));
                if (!tags.Contains("<c>") && !tags.Contains("<c++>")) return false;

                int questionId = int.Parse(id);
                if (!questionIds.Contains(questionId)) questionIds.Add(questionId);
                return false;
            }
            if ("2" != postTypeId) return false;

            string parentId = reader.GetAttribute("ParentId");

            int parId = int.Parse(parentId);
            if (!questionIds.Contains(parId)) return false; /* only c, c++ questions should be on this list */

            string creationDate = reader.GetAttribute("CreationDate");
            string score = reader.GetAttribute("Score");
            string body = reader.GetAttribute("Body");
            string ownerUserId = reader.GetAttribute("OwnerUserId");
            string lastEditorUserId = reader.GetAttribute("LastEditorUserId");
            string lastEditorDisplayName = reader.GetAttribute("LastEditorDisplayName");
            string lastEditDate = reader.GetAttribute("LastEditDate");
            string lastActivityDate = reader.GetAttribute("LastActivityDate");
            string commentCount = reader.GetAttribute("CommentCount");
            string communityOwnedDate = reader.GetAttribute("CommunityOwnedDate");

            List<string> codeBlocks = GetCodeBlocks(body);
            if (codeBlocks == null || codeBlocks.Count == 0) return false;
            int i = 0;

            foreach (string block in codeBlocks)
            {
                if (i++ > 0) outFile.WriteLine(",");

                outFile.Write("(");
                outFile.Write(id);
                outFile.Write(",");
                outFile.Write(parentId);
                outFile.Write(",");
                WriteDate(outFile, creationDate);
                outFile.Write(",");
                outFile.Write(score);
                outFile.Write(",");
                WriteString(outFile, block);
                outFile.Write(",");
                outFile.Write(ownerUserId);
                outFile.Write(",");
                outFile.Write(lastEditorUserId);
                outFile.Write(",");
                WriteString(outFile, lastEditorDisplayName);
                outFile.Write(",");
                WriteDate(outFile, lastEditDate);
                outFile.Write(",");
                WriteDate(outFile, lastActivityDate);
                outFile.Write(",");
                outFile.Write(commentCount);
                outFile.Write(",");
                WriteDate(outFile, communityOwnedDate);
                outFile.Write(")");
            }

            return true;
        }

        private static bool ParsePost(StreamWriter outFile, XmlReader reader)
        {
            string postTypeId = reader.GetAttribute("PostTypeId");
            if ("1" != postTypeId) return false;

            string tags = HttpUtility.HtmlDecode(reader.GetAttribute("Tags"));
            if (!tags.Contains("<c>") && !tags.Contains("<c++>")) return false;

            string id = reader.GetAttribute("Id");
            string acceptedAnswerId = reader.GetAttribute("AcceptedAnswerId");
            string creationDate = reader.GetAttribute("CreationDate");
            string score = reader.GetAttribute("Score");
            string viewCount = reader.GetAttribute("ViewCount");
            string body = reader.GetAttribute("Body");
            string decodedBody = HttpUtility.HtmlDecode(body);
            string ownerUserId = reader.GetAttribute("OwnerUserId");
            string lastEditorUserId = reader.GetAttribute("LastEditorUserId");
            string lastEditorDisplayName = reader.GetAttribute("LastEditorDisplayName");
            string lastEditDate = reader.GetAttribute("LastEditDate");
            string lastActivityDate = reader.GetAttribute("LastActivityDate");
            string title = reader.GetAttribute("Title");
            string answerCount = reader.GetAttribute("AnswerCount");
            string commentCount = reader.GetAttribute("CommentCount");
            string favoriteCount = reader.GetAttribute("FavoriteCount");
            string communityOwnedDate = reader.GetAttribute("CommunityOwnedDate");

            outFile.Write("(");
            outFile.Write(id);
            outFile.Write(",");
            WriteString(outFile, tags);
            outFile.Write(",");
            outFile.Write(acceptedAnswerId);
            outFile.Write(",");
            WriteDate(outFile, creationDate);
            outFile.Write(",");
            outFile.Write(score);
            outFile.Write(",");
            outFile.Write(viewCount);
            outFile.Write(",");
            outFile.Write(ownerUserId);
            outFile.Write(",");
            outFile.Write(lastEditorUserId);
            outFile.Write(",");
            WriteString(outFile, lastEditorDisplayName);
            outFile.Write(",");
            WriteDate(outFile, lastEditDate);
            outFile.Write(",");
            WriteDate(outFile, lastActivityDate);
            outFile.Write(",");
            WriteString(outFile, title);
            outFile.Write(",");
            outFile.Write(answerCount);
            outFile.Write(",");
            outFile.Write(commentCount);
            outFile.Write(",");
            outFile.Write(favoriteCount);
            outFile.Write(",");
            WriteDate(outFile, communityOwnedDate);
            outFile.Write(",");
            WriteString(outFile, null);
            outFile.Write(")");

            return true;
        }

        private static List<string> GetCodeBlocks(string body)
        {
            if (string.IsNullOrWhiteSpace(body)) return null;

            HtmlDocument doc = new HtmlDocument();
            doc.LoadHtml(body);

            HtmlNodeCollection codeBlockCollection = doc.DocumentNode.SelectNodes("pre/code");
            if (codeBlockCollection == null || codeBlockCollection.Count == 0) return null;

            List<string> blocks = new List<string>(codeBlockCollection.Count);

            foreach (HtmlNode node in codeBlockCollection)
            {
                blocks.Add(HttpUtility.HtmlDecode(node.InnerText));
            }

            return blocks;
        }

        private static void WriteString(StreamWriter outFile, string s)
        {
            if (s == null)
            {
                outFile.Write("NULL");
            }
            else
            {
                if (s.IndexOf("'") > 0) s = s.Replace("'", @"\'");
                if (s.IndexOf("\n") > 0) s = s.Replace("\n", "\\n");
                if (s.IndexOf("\r") > 0) s = s.Replace("\r", "\\r");
                outFile.Write("'" + s + "'");
            }
        }

        private static void WriteDate(StreamWriter outFile, string date)
        {
            if (string.IsNullOrWhiteSpace(date))
            {
                outFile.Write("NULL");
            }
            else
            {
                DateTime dateTime = Convert.ToDateTime(date);
                outFile.Write("'" + dateTime.ToString("yyyy-MM-dd H:mm:ss") + "'");
            }
        }
    }
}

from gpt import ai
model_name = "124M" # Overwrite with set_model_name()

chat_ai = ai.ChatAI() # Ready the GPT2 AI generator
chat_ai.load_model() # Load the GPT2 model
#print(chat_ai.get_bot_response(model_name, "Owner", "Hello!"))


    
import http.server
import socketserver
import json

PORT = 6969

class MyHandler(http.server.SimpleHTTPRequestHandler):
    
    def get_response(self, input_data):
        response = None

        rawdata = chat_ai.get_bot_response(model_name, input_data["context"], input_data["name"], input_data["input"])
        print(rawdata)
        data = rawdata.split("ayokadeno:", 1)[1]
        rawoutput = rawdata.splitlines()
        output = []
        for thing in rawoutput:
            if thing == "":
                pass
            else:
                output.append(thing)
        output.pop(0)
        print(output)
        # output is the valid replies
        i = 0
        found = None
        if output[0].split(":", 1)[1].strip() == "":
            while found == None:
                try:
                    if i > 100:
                        response = None
                        break
                    temp = output[i].split(":", 1)
                    if len(temp) == 1:
                        i += 1
                        pass
                    else:
                        temp = temp[1].strip()
                    print(f"data: {temp}")
                    if temp != "":
                        secondline = output[i+1]
                        secondlinesplit = secondline.split(":")
                        if len(secondlinesplit) == 1: # AI added more to the response on a line after whats expected
                            temp += f" {secondlinesplit[0]}"
                            response = temp
                            break
                        elif secondlinesplit == 2: # AI added a second response after the expected one
                            if secondlinesplit[0] == "ayokadeno":
                                temp += f" {secondlinesplit[1]}"
                                response = temp
                                break
                        break
                    i += 1
                except IndexError:
                    response = None
                    break
                
        else:
            response = output[0].split(":", 1)[1]
        return response

    def do_POST(self):
        # - request -
        content_length = int(self.headers['Content-Length'])
        #print('content_length:', content_length)
        
        if content_length:
            input_json = self.rfile.read(content_length)
            input_data = json.loads(input_json)
        else:
            input_data = None
            
        print(input_data)
        response = None
        while response == None:
            
            temp = self.get_response(input_data)
            if temp == None:
                pass
            else:
                response = temp

        
        # - response -
        
        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()


        output_data = {'status': 'OK', 'message': response}
        output_json = json.dumps(output_data)
        
        self.wfile.write(output_json.encode('utf-8'))


Handler = MyHandler


try:
    with socketserver.TCPServer(("localhost", PORT), Handler) as httpd:
        print(f"Starting http://0.0.0.0:{PORT}")
        httpd.serve_forever()
except KeyboardInterrupt:
    print("Stopping by Ctrl+C")
    httpd.server_close()  # to resolve problem `OSError: [Errno 98] Address already in use`
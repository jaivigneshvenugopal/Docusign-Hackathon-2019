import 'package:flutter/material.dart';
import 'dart:io';

class ImageProcessedPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final appTitle = 'Poster Picture/Gif Completed!';
    return Scaffold(
      body: Scaffold(
        appBar: AppBar(
          title: Text(appTitle),
        ),
        body: ProcessedImage(),
      ),
    );
  }
}

class ProcessedImage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: <Widget>[
          Text(
            'Your Poster is ready!',
            style:TextStyle(
              fontStyle: FontStyle.italic,
              fontWeight: FontWeight.bold,
              color: Colors.black87,
              fontSize: 24,
            )
          ),
          SizedBox(height: 20),
          Image.network(
            'https://storage.googleapis.com/docusignbucket/sample4.gif'
          ),
          SizedBox(height: 20),
          Center(
            child: RaisedButton(
              onPressed: () {
                _downloadFile();
              },
              child: Text('Download'),
            ),
          ),
        ]
      )
    );
  }
}

void _downloadFile() {
  HttpClient client = new HttpClient();
  var _downloadData = List<int>();
  var fileSave = new File('./CampaignPoster.gif');

  client.getUrl(Uri.parse('https://storage.googleapis.com/docusignbucket/sample4.gif'))
    .then((HttpClientRequest request) {
      return request.close();
    })
    .then((HttpClientResponse response) {
      response.listen((d) => _downloadData.addAll(d),
        onDone: () {
          fileSave.writeAsBytes(_downloadData);
        }
      );
    });
}




import 'package:flutter/material.dart';
import 'package:flutter/foundation.dart';
import 'PageTile.dart';
import 'ImagePage.dart';
import 'PetitionPage.dart';
import 'DocumentPicker.dart';
import 'ImageProcessedPage.dart';
import 'PetitionLinkPage.dart';

// import 'PageTile.dart';


void main() {
  runApp(new MaterialApp(
    home: new CC50Home(),
    routes: <String, WidgetBuilder> {
      "ImagePage" : (BuildContext context) => new ImagePage(),
      "PetitionPage" : (BuildContext context) => new PetitionPage(),
      "DocumentPicker" : (BuildContext context) => new DocumentPicker(),
      "ImageProcessedPage" : (BuildContext context) => new ImageProcessedPage(),
      "PetitionLinkPage" : (BuildContext context) => new PetitionLinkPage(),
    },
    theme: ThemeData(          // Add the 3 lines from here... 
      primaryColor: Colors.grey[800],
    ),
  ));
} 

class CC50Home extends StatelessWidget {
  @override
  Widget build(BuildContext context) {  
    return new Scaffold(
      appBar: new AppBar(
        title: new Text('CC50 Home'),
      ), 
      body: new Scaffold(
        body: Center(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            mainAxisAlignment: MainAxisAlignment.center,
            mainAxisSize: MainAxisSize.min,
            children: <Widget>[
              Text(
                'Kickstart your CC campaigns',
                style:TextStyle(
                  fontStyle: FontStyle.italic,
                  fontWeight: FontWeight.bold,
                  color: Colors.black87,
                  fontSize: 24,
                )
              ),
              SizedBox(height: 50),
              PageTile(
                title: 'Get Poster',
                onPressed: () {
                  Navigator.of(context).pushNamed("ImagePage");
                },
              ),
              SizedBox(height: 10),
              PageTile(
                title: 'Start Petition',
                onPressed: () {
                  Navigator.of(context).pushNamed("PetitionPage");
                },
              ),
            ],
          )
        ),
      ),
    );
  }
}


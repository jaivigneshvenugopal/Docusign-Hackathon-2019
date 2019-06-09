import 'package:flutter/material.dart';
import 'package:flutter/foundation.dart';
import 'dart:async';
import 'dart:io';
import 'package:image_picker/image_picker.dart';

// class ImagePage extends StatelessWidget {
//   @override
//   _ImagePageState createState() => new _ImagePageState();
// }

class ImagePage extends StatefulWidget {
  @override
  State<StatefulWidget> createState() {
    return new _ImagePageState();
  }
}

class _ImagePageState extends State<ImagePage> {
//Final file chosen - whether through Gallery or Camera
  File finalFile;

//save the result of gallery file
  File galleryFile;

//save the result of camera file
  File cameraFile;

  @override
  Widget build(BuildContext context) {
    //display image selected from gallery
    imageSelectorGallery() async {
      galleryFile = await ImagePicker.pickImage(
        source: ImageSource.gallery,
        // maxHeight: 50.0,
        // maxWidth: 50.0,
      );
      finalFile = galleryFile;
      print("You selected gallery image : " + galleryFile.path);
      setState(() {});
    }

    //display image selected from camera
    imageSelectorCamera() async {
      cameraFile = await ImagePicker.pickImage(
        source: ImageSource.camera,
        //maxHeight: 50.0,
        //maxWidth: 50.0,
      );
      finalFile = cameraFile;
      print("You selected camera image : " + cameraFile.path);
      setState(() {});
    }

    return new Scaffold(
      appBar: new AppBar(
        title: new Text('Image Picker'),
      ),
      body: new Builder(
        builder: (BuildContext context) {
          return new Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              Text(
                'Create Climate Change Poster',
                style:TextStyle(
                  color: Colors.black87,
                  fontSize: 24,
                )
              ),
              SizedBox(height: 50),
              new RaisedButton(
                child: new Text('Select Image from Gallery'),
                onPressed: imageSelectorGallery,
              ),
              SizedBox(height: 10),
              new RaisedButton(
                child: new Text('Select Image from Camera'),
                onPressed: imageSelectorCamera,
              ),
              SizedBox(height: 10),
              displaySelectedFile(finalFile),
              SizedBox(height: 10),
              new RaisedButton(
                child: new Text('Process'),
                onPressed:() {
                  Navigator.of(context).pushNamed("ImageProcessedPage");
                },
              ),
            ],
          );
        },
      ),
    );
  }

  Widget displaySelectedFile(File file) {
    return new Center(
      child: SizedBox(
        height: 200.0,
        width: 300.0,
  //child: new Card(child: new Text(''+galleryFile.toString())),
  //child: new Image.file(galleryFile),
        child: file == null
            ? new Text('Selected:')
            : new Image.file(file),
      )
    );
  }
}


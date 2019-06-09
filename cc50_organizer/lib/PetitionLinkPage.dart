import 'package:flutter/material.dart';
import 'package:flutter_linkify/flutter_linkify.dart';
import 'package:url_launcher/url_launcher.dart';

class PetitionLinkPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    var url = 'https://demo.docusign.net/Signing/?ti=8237ec7cbe0248c98df0c1789107fbfc';
    return new Scaffold(
      body: Center (
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children:<Widget>[
            Text("Share this link to begin petitioning!"),
            SizedBox(height: 30),
            Padding(
              padding: const EdgeInsets.only(left:50.0),
              child: Linkify(
                text: '${url}',
                onOpen: (url) async {
                  if (await canLaunch(url)) {
                    await launch(url);
                  } else {
                    throw 'Could not launch $url';
                  }
                },
                style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16.0),
              ),
            ),
            new Padding(
              padding: const EdgeInsets.only(top: 10.0, bottom: 10.0),
              child: RaisedButton(
                onPressed: () {
                  Navigator.pop(context);
                },
                child: Text('Back'),
              ),
            ),
          ],
        )
      )
    );
  }
}

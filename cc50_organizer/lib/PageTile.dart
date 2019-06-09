import 'package:flutter/material.dart';
import 'package:flutter/foundation.dart';

class PageTile extends StatelessWidget {
  PageTile({
    @required this.onPressed, 
    @required this.title,
    });

  final GestureTapCallback onPressed;
  final String title;

  @override
  Widget build(BuildContext context) {
    return ButtonTheme(
      minWidth: 250.0,
      height: 200.0,
      child: RaisedButton (
        child: Text(
          this.title,
          style:TextStyle(
            color: Colors.white,
            fontSize: 24,
          )
        ),
        color: Colors.green[800],
        highlightColor: Colors.lightGreen[600],
        onPressed: onPressed,
        padding: EdgeInsets.symmetric(vertical: 80.0),
        shape: new RoundedRectangleBorder(borderRadius: new BorderRadius.circular(15.0)),
      ),
    );
  }
}

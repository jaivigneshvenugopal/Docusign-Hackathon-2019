import 'package:flutter/material.dart';
import 'package:flutter/foundation.dart';
import 'package:file_picker/file_picker.dart';


class PetitionPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final appTitle = 'Enter Details to Create Petition';

    return Scaffold(
      body: Scaffold(
        appBar: AppBar(
          title: Text(appTitle),
        ),
        body: PetitionForm(),
      ),
    );
  }
}

// Create a Form Widget
class PetitionForm extends StatefulWidget {
  @override
  PetitionFormState createState() {
    return PetitionFormState();
  }
}

// Create a corresponding State class. This class will hold the data related to
// the form.
class PetitionFormState extends State<PetitionForm> {
  // Create a global key that will uniquely identify the Form widget and allow
  // us to validate the form
  //
  // Note: This is a GlobalKey<FormState>, not a GlobalKey<MyPetitionFormState>!
  final _formKey = GlobalKey<FormState>();

  @override
  Widget build(BuildContext context) {
    // Build a Form widget using the _formKey we created above
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      mainAxisAlignment: MainAxisAlignment.center,
      children: <Widget>[
        Center(
          child: Padding(
            padding: const EdgeInsets.all(12.0),
            child: Text(
              'Get Signatures!',
              style:TextStyle(
                color: Colors.green[800],
                fontSize: 32,
              )
            ),
          ),
        ),
        Center(
          child: Padding(
            padding: const EdgeInsets.all(24.0),
              child: Text(
              'Select the documents that you wish to petition and gain signatures for. ' +
              'CC50 and Docusign will generate a link that directs viewers to your petition documents, allowing them to sign.',
              style:TextStyle(
                color: Colors.green[500],
                fontSize: 18,
              )
            ),
          ),
        ),
        Center(
          child: Padding(
            padding: const EdgeInsets.symmetric(vertical: 16.0),
            child: RaisedButton(
              onPressed: () {
                Navigator.of(context).pushNamed("DocumentPicker");
              },
              child: Text('Select Documents'),
            ),
          ),
        ),
        
        // Form(
        //   key: _formKey,
        //   child: Column(
        //     children: <Widget>[
        //       Padding(
        //         padding: EdgeInsets.all(15.0),
        //         child: TextFormField(
        //           decoration: new InputDecoration(
        //             labelText: "Petition Organizer's Name",
        //             fillColor: Colors.white,
        //             border: new OutlineInputBorder(
        //               borderRadius: new BorderRadius.circular(25.0),
        //               borderSide: new BorderSide(
        //               ),
        //             ),
        //           ),
        //           validator: (value) {
        //             if (value.isEmpty) {
        //               return 'Please enter some text';
        //             }
        //             return null;
        //           },
        //         ),
        //       ),
              
        //       Padding(
        //         padding: EdgeInsets.all(15.0),
        //         child: TextFormField(
        //           decoration: new InputDecoration(
        //             labelText: "Petition Organizer's Email",
        //             fillColor: Colors.white,
        //             border: new OutlineInputBorder(
        //               borderRadius: new BorderRadius.circular(25.0),
        //               borderSide: new BorderSide(
        //               ),
        //             ),
        //           ),
        //           validator: (value) {
        //             if (value.isEmpty) {
        //               return 'Please enter some text';
        //             }
        //             return null;
        //           },
        //         ),
        //       ),

        //       Padding(
        //         padding: const EdgeInsets.symmetric(vertical: 16.0),
        //         child: RaisedButton(
        //           onPressed: () {
        //             Navigator.of(context).pushNamed("DocumentPicker");
        //           },
        //           child: Text('Select Petition Document(s)'),
        //         ),
        //       ),

        //       
        //     ],
        //   ),
        // ),
        Center(
          child: RaisedButton(
            onPressed: () {
              Navigator.pop(context);
            },
            child: Text('Back'),
          ),
        ),
      ],
    );
  }
}

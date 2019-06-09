import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:file_picker/file_picker.dart';

class DocumentPicker extends StatefulWidget {
  @override
  _DocumentPickerState createState() => new _DocumentPickerState();
}

class _DocumentPickerState extends State<DocumentPicker> {
  String _fileName;
  String _path;
  Map<String, String> _paths;
  String _extension;
  bool _multiPick = false;
  bool _hasValidMime = false;
  FileType _pickingType;
  TextEditingController _controller = new TextEditingController();

  @override
  void initState() {
    super.initState();
    _controller.addListener(() => _extension = _controller.text);
  }

  void _openFileExplorer() async {
    if (_pickingType != FileType.CUSTOM || _hasValidMime) {
      try {
        if (_multiPick) {
          print('multi');
          _path = null;
          _paths = await FilePicker.getMultiFilePath(type: FileType.ANY, fileExtension: 'pdf');
        } else {
          print('single');
          _paths = null;
          _path = await FilePicker.getFilePath(type: FileType.ANY, fileExtension: 'pdf');
        }
      } on PlatformException catch (e) {
        print("Unsupported operation" + e.toString());
      }
      if (!mounted) return;

      setState(() {
        _fileName = _path != null ? _path.split('/').last : _paths != null ? _paths.keys.toString() : '...';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return new Scaffold(
      appBar: new AppBar(
        title: const Text('Choose Petition Documents for Signing'),
      ),
      body: new Center(
          child: new Padding(
        padding: const EdgeInsets.only(left: 10.0, right: 10.0),
        child: new Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            new Padding(
              padding: const EdgeInsets.only(top:10.0, bottom: 10.0),
              child: new Text('Select PDF documents to include in your petition bundle'),
            ),
            new ConstrainedBox(
              constraints: BoxConstraints.tightFor(width: 200.0),
              child: new SwitchListTile.adaptive(
                title: new Text('Pick multiple files', textAlign: TextAlign.right),
                onChanged: (bool value) => setState(() => _multiPick = value),
                value: _multiPick,
              ),
            ),
            new Padding(
              padding: const EdgeInsets.only(top: 10.0, bottom: 10.0),
              child: new RaisedButton(
                onPressed: () => _openFileExplorer(),
                child: new Text("Open file picker"),
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
            new Builder(
              builder: (BuildContext context) => new Container(
                padding: const EdgeInsets.only(bottom: 30.0),
                height: MediaQuery.of(context).size.height * 0.50,
                child: new Scrollbar(
                  child: _path != null || _paths != null
                    ? new ListView.separated(
                        itemCount: _paths != null && _paths.isNotEmpty ? _paths.length : 1,
                        itemBuilder: (BuildContext context, int index) {
                          final bool isMultiPath = _paths != null && _paths.isNotEmpty;
                          final String name = 'File $index: ' + (isMultiPath ? _paths.keys.toList()[index] : _fileName ?? '...');
                          final path = isMultiPath ? _paths.values.toList()[index].toString() : _path;

                          return new ListTile(
                            title: new Text(
                              name,
                            ),
                            // subtitle: new Text(path),
                          );
                        },
                        separatorBuilder: (BuildContext context, int index) => new Divider(),
                      )
                    : new Container(),
                ),
              ),
            ),
            new Padding(
              padding: const EdgeInsets.only(top: 10.0, bottom: 20.0),
              child: RaisedButton(
                onPressed: () {
                  Navigator.of(context).pushNamed("PetitionLinkPage");
                },
                child: Text('Generate Link'),
              ),
            ),
          ],
        ),
      )),
    );
  }
}

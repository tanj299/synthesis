import 'dart:convert';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:lets_head_out/Screens/DashBoard.dart';
import 'package:lets_head_out/utils/Buttons.dart';
import 'package:lets_head_out/utils/TextStyles.dart';
import 'package:lets_head_out/utils/consts.dart';
import 'package:lets_head_out/utils/forms.dart';
import 'package:http/http.dart' as http;

class AddPlantPage extends StatefulWidget {
  final String email;

  AddPlantPage({
    Key key,
    @required this.email,
  }) : super(key: key);

  @override
  _AddPlantPageState createState() => _AddPlantPageState();
}

// class AddList {
//   List plants;

//   AddList({
//     this.plants,
//   });

//   factory AddList.fromJson(List<dynamic> parsedJson) {
//     return new AddList(plants: parsedJson);
//   }
// }

// PlantRequest - parses json to water plant through /requests in backend
class PlantRequest {
  final String userEmail;
  final String plantName;
  final String species;
  final String serialPort;
  final String position;
  final String currPhoto;
  final String waterThreshold;
  final String lightThreshold;

  PlantRequest({
    this.userEmail,
    this.plantName,
    this.species,
    this.serialPort,
    this.position,
    this.currPhoto,
    this.waterThreshold,
    this.lightThreshold,
  });

  factory PlantRequest.fromJson(Map<String, dynamic> json) {
    return PlantRequest(
      userEmail: json['user_email'],
      plantName: json['plant_name'],
      species: json['species'],
      serialPort: json['serial_port'],
      position: json['position'],
      currPhoto: json['curr_photo'],
      waterThreshold: json['water_threshold'],
      lightThreshold: json['light_threshold'],
    );
  }
}

Future<PlantRequest> addPlant(
    String userEmail,
    String plantName,
    String species,
    String serialPort,
    int position,
    int currPhoto,
    int waterThreshold,
    int lightThreshold) async {
      final http.Response response = await http.post(
    // 'http://localhost:5000/plants/insert',
    'http://backend-dev222222.us-east-1.elasticbeanstalk.com/plants/insert',
    headers: <String, String>{
      'Content-Type': 'application/json; charset=UTF-8',
    },
    body: jsonEncode(<String, String>{
      "user_email": userEmail,
      "plant_name": plantName,
      "species": species,
      "serial_port": serialPort,
      "position": position.toString(),
      "curr_photo": currPhoto.toString(),
      "water_threshold": waterThreshold.toString(),
      "light_threshold": lightThreshold.toString(),
    }),
  );
  
  if (response.statusCode == 200) {
    return PlantRequest.fromJson(jsonDecode(response.body));
  } else {
    throw Exception('Failed to load plant request');
  }
}

class _AddPlantPageState extends State<AddPlantPage> {
  String plantName;
  String species;
  String userEmail;
  String uri;
  String serialPort;
  String position;
  String currPhoto;
  String waterThreshold;
  String lightThreshold;

  @override
  void initState() {
    super.initState();
    plantName = "";
    species = "";
    userEmail = "janesmith.synthesis@gmail.com";
    uri = "";
    serialPort = "";
    position = "1";
    currPhoto = "1";
    waterThreshold = "0";
    lightThreshold = "0";
  }

  void updateValue(name, value) {
    if (name == 'plantName') {
      plantName = value;
    } else if (name == 'species') {
      species = value;
    } else if (name == 'userEmail') {
      userEmail = value;
    } else if (name == 'serialPort') {
      serialPort = value;
    } else if (name == 'position') {
      position = value;
    } else if (name == 'currPhoto') {
      currPhoto = value;
    } else if (name == 'waterThreshold') {
      waterThreshold = value;
    } else if (name == 'lightThreshold') {
      lightThreshold = value;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        body: Stack(children: <Widget>[
      Container(
        decoration: BoxDecoration(
            image: DecorationImage(
                image: AssetImage("assets/bgimg_dashboard.jpg"),
                fit: BoxFit.cover)),
        child: Scaffold(
            backgroundColor: Colors.transparent,
            appBar: AppBar(
              elevation: 0,
              backgroundColor: Colors.transparent,
            ),
            body: SingleChildScrollView(
                // child: Center(
                child: Align(
                    // alignment: Alignment.centerLeft,
                    child: Column(children: <Widget>[
              SizedBox(height: 20),
              Container(
                  width: 340.0,
                  child: EditForm(Icons.person, plantName, "Name", "plantName",
                      updateValue)),
              SizedBox(height: 20),
              Container(
                  width: 340.0,
                  child: EditForm(FontAwesomeIcons.seedling, species, "Species",
                      "species", updateValue)),
              SizedBox(height: 20),
              Container(
                  width: 340.0,
                  child: EditForm(Icons.enhanced_encryption, serialPort,
                      "Serial port", "serialPort", updateValue)),
              SizedBox(height: 20),
              Container(
                width: 340.0,
                child: EditForm(Icons.crop_square, position,
                    "Position", "position", updateValue),
              ),
              SizedBox(height: 20),
              Container(
                width: 340.0,
                child: EditForm(FontAwesomeIcons.water, waterThreshold,
                    "Water threshold", "waterThreshold", updateValue),
              ),
              SizedBox(height: 20),
              Container(
                width: 340.0,
                child: EditForm(FontAwesomeIcons.lightbulb, lightThreshold,
                    "Light threshold", "lightThreshold", updateValue),
              ),
              SizedBox(height: 60),
              WideButtonGreen("Add Plant", () {
                addPlant(
                    userEmail,
                    plantName,
                    species,
                    serialPort,
                    int.parse(position),
                    int.parse(currPhoto),
                    int.parse(waterThreshold),
                    int.parse(lightThreshold));
                Navigator.pop(context);
              }),
              SizedBox(height: 40),
            ])))),
      )
    ]));
  }
}

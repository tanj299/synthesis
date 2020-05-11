import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:lets_head_out/utils/TextStyles.dart';
import 'package:lets_head_out/utils/consts.dart';

import 'dart:convert';
import 'package:http/http.dart' as http;

class PopUp extends StatefulWidget {
  final int plantId;
  PopUp({Key key, @required this.plantId}) : super(key: key);

  @override
  _PopUpState createState() => _PopUpState();
}

class PlantLogList {
  final List<PlantLog> plants;
  PlantLogList({
    this.plants,
  });
  factory PlantLogList.fromJson(List<dynamic> parsedJson) {
    List<PlantLog> plants = new List<PlantLog>();
    plants =
        parsedJson.map((plantJson) => PlantLog.fromJson(plantJson)).toList();
    return new PlantLogList(plants: plants);
  }
}

class PlantLog {
  final String plantId;
  final String timestamp;
  final String category;

  // constructor
  PlantLog({
    this.plantId,
    this.timestamp,
    this.category,
  });

  factory PlantLog.fromJson(Map<String, dynamic> json) {
    return PlantLog(
      plantId: json['plant_id'].toString(),
      timestamp: json['timestamp'],
      category: json['category'],
    );
  }
}
// end Plant

// http://localhost:5000/requests/all/1/2020-04-30%2004:10:38
Future<PlantLogList> fetchPlantInfo(id) async {
  final response = await http
      .get('http://localhost:5000/requests/all/${id}/2020-04-30%2004:10:38');

  if (response.statusCode == 200) {
    return PlantLogList.fromJson(jsonDecode(response.body));
  } else {
    throw Exception('Failed to load plant');
  }
}
// end fetchPlantInfo

class _PopUpState extends State<PopUp> {
  Future<PlantLogList> futurePlantLogList;
  @override
  void initState() {
    super.initState();
    futurePlantLogList = fetchPlantInfo(widget.plantId);
  }

  Widget build(BuildContext context) {
    return new AlertDialog(
      title: const Text('Latest plant logs'),
      content: new Container(
          height: 300,
          width: 300,
          child: FutureBuilder<PlantLogList>(
            future: futurePlantLogList,
            builder: (context, snapshot) {
              if (snapshot.hasData) {
                int numPlants = snapshot
                    .data.plants.length; // returns length of plants array
                List<Widget> plantsRender = new List<Widget>();
                for (var j = 0; j < numPlants; j++) {
                  int i = numPlants -
                      j - 1; // do in descending order to get most recent first
                  plantsRender.add(BoldText(
                      (j+1).toString() + ") " + snapshot.data.plants[i].timestamp +
                          " - " +
                          snapshot.data.plants[i].category,
                      15.0,
                      Colors.black));
                  plantsRender.add(SizedBox(
                    height: 5.0,
                  ));
                }
                return Container(
                  child: ListView(
                    scrollDirection: Axis.vertical,
                    children: plantsRender,
                  ),
                );
              }
              // error
              else if (snapshot.hasError) {
                return Text("${snapshot.error}");
              }
              // By default, show a loading spinner.
              return CircularProgressIndicator();
            },
          )
          // ],
          ),
      actions: <Widget>[
        new FlatButton(
          onPressed: () {
            Navigator.of(context).pop();
          },
          textColor: Theme.of(context).primaryColor,
          child: const Text('Back'),
        ),
      ],
    );
  }
}

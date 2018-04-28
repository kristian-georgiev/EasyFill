// import React from 'react';
// 'use strict';
import React, { Component } from 'react';
import { StyleSheet, Text, View } from 'react-native';

import { Button } from 'react-native-elements';
import Icon from 'react-native-vector-icons/FontAwesome';

// import {
//   AppRegistry,
//   Dimensions,
//   StyleSheet,
//   Text,
//   TouchableOpacity,
//   View
// } from 'react-native';
// import { RNCamera } from 'react-native-camera';

// class App extends Component {
//   render() {
//     return (
//       <View style={styles.container}>
//         <RNCamera
//           ref={ref => {
//             this.camera = ref;
//           }}
//           style={styles.preview}
//           type={RNCamera.Constants.Type.back}
//           flashMode={RNCamera.Constants.FlashMode.on}
//           permissionDialogTitle={'Permission to use camera'}
//           permissionDialogMessage={'We need your permission to use your camera phone'}
//         />
//         <View style={{ flex: 0, flexDirection: 'row', justifyContent: 'center', }}>
//           <TouchableOpacity
//             onPress={this.takePicture.bind(this)}
//             style={styles.capture}
//           >
//             <Text style={{ fontSize: 14 }}> SNAP </Text>
//           </TouchableOpacity>
//         </View>
//       </View>
//     );
//   }

//   takePicture = async function () {
//     if (this.camera) {
//       const options = { quality: 0.5, base64: true };
//       const data = await this.camera.takePictureAsync(options)
//       console.log(data.uri);
//     }
//   };
// }

// const styles = StyleSheet.create({
//   container: {
//     flex: 1,
//     flexDirection: 'column',
//     backgroundColor: 'black'
//   },
//   preview: {
//     flex: 1,
//     justifyContent: 'flex-end',
//     alignItems: 'center'
//   },
//   capture: {
//     flex: 0,
//     backgroundColor: '#fff',
//     borderRadius: 5,
//     padding: 15,
//     paddingHorizontal: 20,
//     alignSelf: 'center',
//     margin: 20
//   }
// });

// AppRegistry.registerComponent('App', () => App);


// import Camera from 'react-native-camera';


// export default class App extends Component {
//   render() {
//     return (
//       <Screen>
//         <Camera style={{ flex: 1 }}
//           ref={cam => this.camera = cam}
//           aspect={Camera.constants.Aspect.fill}>

//         </Camera>
//       </Screen>
//     );
//   }
// }


export default class App extends React.Component {
  render() {
    return (
      <View id="yes be" style={styles.container}>
        <Button
          title='Aidee'
        />
        <Button
          icon={
            <Icon
              name='arrow-right'
              size={15}
              color='white'
            />
          }
          title='BUTTON WITH ICON'
        />
        <Text>Dai go na eks, kuchko.</Text>
        <Text>Are de.</Text>
        <Text>Obas.</Text>
        <Text>Shake your phone to open the developer menu.</Text>
      </View>
    );
  }
}


const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#00FFFF',
    alignItems: 'center',
    justifyContent: 'center',
  },
});

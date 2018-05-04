import React from 'react';
import { CameraRoll, Image,  ListView, Text, View, StyleSheet, Dimensions, Button, TouchableOpacity, Vibration} from 'react-native';
import { StackNavigator } from 'react-navigation';
import { Camera, Permissions, Constants, takeSnapshotAsync, FileSystem} from 'expo';
import GalleryScreen from './GalleryScreen';
import isIPhoneX from 'react-native-is-iphonex';

class HomeScreen extends React.Component {
  render() {
    return (
        <View style={styles.container}>

          <View style={styles.containerRow}>
            <TouchableOpacity style={styles.gridItem} onPress={() => this.props.navigation.navigate('Next')}>
                <Text>HELP</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.gridItem} onPress={() => this.props.navigation.navigate('Next')}>
                <Text>PRINT</Text>
            </TouchableOpacity>
          </View>

          <View style={styles.containerRow}>
            <TouchableOpacity style={styles.gridItem} onPress={() => this.props.navigation.navigate('Next')}>
                <Text>BACK</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.gridItem} onPress={() => this.props.navigation.navigate('Next')}>
                <Text>NEXT</Text>
            </TouchableOpacity>
          </View>

          <View style={styles.containerRow}>
            <TouchableOpacity style={styles.gridItem} onPress={() => this.props.navigation.navigate('Next')}>
                <Text>REPEAT</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.gridItem} onPress={() => this.props.navigation.navigate('Next')}>
                <Text>FILL</Text>
            </TouchableOpacity>
          </View>

        

        </View>

    );
  }
}

// camera screen - from https://github.com/expo/camerja
class CameraScreen extends React.Component {
  state = {
    zoom: 0,
    autoFocus: 'on',
    type: 'back',
    whiteBalance: 'auto',
    ratio: '16:9',
    ratios: [],
    photoId: 1,
    showGallery: false,
    photos: [],
    permissionsGranted: false,
  };

  async componentWillMount() {
    const { status } = await Permissions.askAsync(Permissions.CAMERA);
    this.setState({ permissionsGranted: status === 'granted' });
  }

  componentDidMount() {
    FileSystem.makeDirectoryAsync(FileSystem.documentDirectory + 'photos').catch(e => {
      console.log(e, 'Directory exists');
    });
  }

  getRatios = async () => {
    const ratios = await this.camera.getSupportedRatios();
    return ratios;
  };

  toggleView() {
    this.setState({
      showGallery: !this.state.showGallery,
    });
  }

  // takes and saves photo
  takePicture = async function() {
    if (this.camera) {
      this.camera.takePictureAsync().then(data => {
        FileSystem.moveAsync({
          from: data.uri,
          to: `${FileSystem.documentDirectory}photos/Photo_${this.state.photoId}.jpg`,
        }).then(() => {
          // let saveResult = CameraRoll.saveToCameraRoll(this.state.photoId,'photo'); //-> trying to get this to save pic to camera roll
          this.setState({
            photoId: this.state.photoId, // add + 1 to save more than 1 photo
          });
          Vibration.vibrate();
        });
      });
    }
  };



  // Shows the picture after it is taken
  renderGallery() {
    return <GalleryScreen onPress={this.toggleView.bind(this)} />;
  }

  // if not granted permission to open camera
  renderNoPermissions() {
    return (
      <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center', padding: 10 }}>
        <Text style={{ color: 'white' }}>
          Camera permissions not granted - cannot open camera preview.
        </Text>
      </View>
    );
  }

  renderCamera() {
    return (
      <Camera
        ref={ref => {
          this.camera = ref;
        }}
        style={{
          flex: 1,
        }}
        type={this.state.type}
        autoFocus={this.state.autoFocus}
        whiteBalance={this.state.whiteBalance}
        ratio={this.state.ratio}>
        <View
          style={{
            flex: 0.4,
            backgroundColor: 'transparent',
            flexDirection: 'row',
            alignSelf: 'flex-end',
            marginBottom: -5,
          }}>
        </View>
        <View
          style={{
            flex: 0.1,
            paddingBottom: isIPhoneX ? 20 : 0,
            backgroundColor: 'transparent',
            flexDirection: 'row',
            alignSelf: 'flex-end',
          }}>
          <TouchableOpacity
            style={[styles.flipButton, { flex: 0.3, alignSelf: 'flex-end' }]}
            onPress={this.takePicture.bind(this)}>
            <Text style={styles.flipText}> SNAP </Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.flipButton, { flex: 0.25, alignSelf: 'flex-end' }]}
            onPress={this.toggleView.bind(this)}>
            <Text style={styles.flipText}> Gallery </Text>
          </TouchableOpacity>

        </View>
      </Camera>
    );
  }

  render() {
    const cameraScreenContent = this.state.permissionsGranted
      ? this.renderCamera()
      : this.renderNoPermissions();
    const content = this.state.showGallery ? this.renderGallery() : cameraScreenContent;
    return <View style={styles.container}>{content}</View>;
  }
}


// keeps track of screen flow
const Navigator = StackNavigator({
  Home: { screen: HomeScreen },
  Next: { screen: CameraScreen }})

// 1
export default class App extends React.Component {
  render() {
    return (
      <View style={styles.container}>
        <Navigator style={{ }} />
      </View>
    );
  }
}

const styles = StyleSheet.create({
  // entire screen's view - should be all black theoretically
  container: {
    flex: 1,
    backgroundColor: "#000000",
    width: Dimensions.get('window').width,
    height: Dimensions.get('window').height,
  },

  // each row
  containerRow: {
    flex: 1,
    flexDirection: "row",
    backgroundColor: '#fff',
  },
  gridItem: {
    margin: 2,
    height: Dimensions.get('window').height / 3,
    backgroundColor: "#A9A9A9",
    width: Dimensions.get('window').width / 2, //Device width divided in almost a half
    justifyContent: 'center',
    alignItems: 'center',
  },

  // new stuff
  gallery: {
    flex: 1,
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  flipButton: {
    flex: 0.3,
    height: 40,
    marginHorizontal: 2,
    marginBottom: 10,
    marginTop: 20,
    borderRadius: 8,
    backgroundColor: 'darkseagreen',
    borderColor: 'white',
    borderWidth: 1,
    padding: 5,
    alignItems: 'center',
    justifyContent: 'center',
  },
  flipText: {
    color: 'white',
    fontSize: 15,
  },
});



//useful links:
//screen flow help from: https://stackoverflow.com/questions/45369861/stacknavigator-in-react-native-app
// cameraview: https://docs.expo.io/versions/latest/sdk/camera;
// camerasaveasjpg: https://snack.expo.io/SJRvlSxvb
// other effects: https://github.com/expo/camerja (also has pretty buttons lol)



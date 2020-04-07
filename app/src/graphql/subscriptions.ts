// tslint:disable
// eslint-disable
// this is an auto generated file. This will be overwritten

export const onCreateBarks = /* GraphQL */ `
  subscription OnCreateBarks(
    $deviceId: String
    $timestamp: Int
    $probability: String
    $camera: String
    $wav_file: String
  ) {
    onCreateBarks(
      deviceId: $deviceId
      timestamp: $timestamp
      probability: $probability
      camera: $camera
      wav_file: $wav_file
    ) {
      deviceId
      timestamp
      probability
      camera
      wav_file
    }
  }
`;
export const onUpdateBarks = /* GraphQL */ `
  subscription OnUpdateBarks(
    $deviceId: String
    $timestamp: Int
    $probability: String
    $camera: String
    $wav_file: String
  ) {
    onUpdateBarks(
      deviceId: $deviceId
      timestamp: $timestamp
      probability: $probability
      camera: $camera
      wav_file: $wav_file
    ) {
      deviceId
      timestamp
      probability
      camera
      wav_file
    }
  }
`;
export const onDeleteBarks = /* GraphQL */ `
  subscription OnDeleteBarks(
    $deviceId: String
    $timestamp: Int
    $probability: String
    $camera: String
    $wav_file: String
  ) {
    onDeleteBarks(
      deviceId: $deviceId
      timestamp: $timestamp
      probability: $probability
      camera: $camera
      wav_file: $wav_file
    ) {
      deviceId
      timestamp
      probability
      camera
      wav_file
    }
  }
`;

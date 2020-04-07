// tslint:disable
// eslint-disable
// this is an auto generated file. This will be overwritten

export const getBarks = /* GraphQL */ `
  query GetBarks($deviceId: String!, $timestamp: Int!) {
    getBarks(deviceId: $deviceId, timestamp: $timestamp) {
      deviceId
      timestamp
      probability
      camera
      wav_file
    }
  }
`;
export const listBarks = /* GraphQL */ `
  query ListBarks(
    $filter: TableBarksFilterInput
    $limit: Int
    $nextToken: String
  ) {
    listBarks(filter: $filter, limit: $limit, nextToken: $nextToken) {
      items {
        deviceId
        timestamp
        probability
        camera
        wav_file
      }
      nextToken
    }
  }
`;

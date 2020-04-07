// tslint:disable
// eslint-disable
// this is an auto generated file. This will be overwritten

export const getBarks = /* GraphQL */ `
  query GetBarks($camera: String!, $timestamp: Int!) {
    getBarks(camera: $camera, timestamp: $timestamp) {
      camera
      timestamp
      probability
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
        camera
        timestamp
        probability
        wav_file
      }
      nextToken
    }
  }
`;

/* tslint:disable */
/* eslint-disable */
//  This file was automatically generated and should not be edited.

export type TableBarksFilterInput = {
  camera?: TableStringFilterInput | null,
  timestamp?: TableIntFilterInput | null,
  probability?: TableStringFilterInput | null,
  wav_file?: TableStringFilterInput | null,
};

export type TableStringFilterInput = {
  ne?: string | null,
  eq?: string | null,
  le?: string | null,
  lt?: string | null,
  ge?: string | null,
  gt?: string | null,
  contains?: string | null,
  notContains?: string | null,
  between?: Array< string | null > | null,
  beginsWith?: string | null,
};

export type TableIntFilterInput = {
  ne?: number | null,
  eq?: number | null,
  le?: number | null,
  lt?: number | null,
  ge?: number | null,
  gt?: number | null,
  contains?: number | null,
  notContains?: number | null,
  between?: Array< number | null > | null,
};

export type GetBarksQueryVariables = {
  camera: string,
  timestamp: number,
};

export type GetBarksQuery = {
  getBarks:  {
    __typename: "Barks",
    camera: string,
    timestamp: number,
    probability: string,
    wav_file: string,
  } | null,
};

export type ListBarksQueryVariables = {
  filter?: TableBarksFilterInput | null,
  limit?: number | null,
  nextToken?: string | null,
};

export type ListBarksQuery = {
  listBarks:  {
    __typename: "BarksConnection",
    items:  Array< {
      __typename: "Barks",
      camera: string,
      timestamp: number,
      probability: string,
      wav_file: string,
    } | null > | null,
    nextToken: string | null,
  } | null,
};

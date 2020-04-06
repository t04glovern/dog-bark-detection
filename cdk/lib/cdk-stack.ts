import cdk = require('@aws-cdk/core');
import certificatemanager = require('@aws-cdk/aws-certificatemanager');
import cloudfront = require('@aws-cdk/aws-cloudfront');
import codebuild = require('@aws-cdk/aws-codebuild');
import iam = require('@aws-cdk/aws-iam');
import s3 = require('@aws-cdk/aws-s3');

export class CdkStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // S3 Bucket
    const bucket = new s3.Bucket(this, 'bucket', {
      bucketName: 'barks.devopstar.com'
    });

    const certificate = new certificatemanager.Certificate(this, 'certificate', {
      domainName: 'barks.devopstar.com',
      subjectAlternativeNames: ['www.barks.devopstar.com'],
      validationMethod: certificatemanager.ValidationMethod.DNS,
    });

    const distribution = new cloudfront.CloudFrontWebDistribution(this, 'cloudfront', {
      originConfigs: [{
        s3OriginSource: {
          s3BucketSource: bucket
        },
        behaviors: [{
          isDefaultBehavior: true
        }]
      }],
      errorConfigurations: [
        {
          errorCode: 403,
          responseCode: 404,
          errorCachingMinTtl: 0,
          responsePagePath: '/404.html'
        }
      ],
      viewerCertificate: cloudfront.ViewerCertificate.fromAcmCertificate(
        certificate,
        {
          aliases: ['barks.devopstar.com', 'www.barks.devopstar.com'],
          securityPolicy: cloudfront.SecurityPolicyProtocol.TLS_V1,
          sslMethod: cloudfront.SSLMethod.SNI,
        }
      ),
    });

    // CloudWatch Log Read/Write Access
    const log_policy = new iam.PolicyStatement({
      actions: [
        'logs:CreateLogGroup',
        'logs:CreateLogStream',
        'logs:PutLogEvents',
      ],
      resources: [
        `arn:aws:logs:${cdk.Aws.REGION}:${cdk.Aws.ACCOUNT_ID}:/aws/codebuild/*`,
      ]
    });

    // CloudFront Invalidation Access
    const cloudfront_policy = new iam.PolicyStatement({
      actions: [
        'cloudfront:CreateInvalidation',
      ],
      resources: [
        '*'
      ]
    });

    //
    // Source - (GitHub_Source)
    //
    const gitHubSource = codebuild.Source.gitHub({
      owner: 't04glovern',
      repo: 'dog-bark-detection',
      webhookFilters: [
        codebuild.FilterGroup.inEventOf(codebuild.EventAction.PUSH).andBranchIs('master')
      ],
      reportBuildStatus: true,
      webhook: true
    });

    //
    // CodeBuild - Build
    //
    const buildProject = new codebuild.Project(this, 'codebuild', {
      badge: true,
      projectName: 'barks-devopstar-build',
      buildSpec: codebuild.BuildSpec.fromSourceFilename('buildspec.yml'),
      source: gitHubSource,
      cache: codebuild.Cache.bucket(new s3.Bucket(this, 'codebuild-cache')),
      environment: {
        buildImage: codebuild.LinuxBuildImage.UBUNTU_14_04_NODEJS_10_14_1,
        environmentVariables: {
          CLOUDFRONT_DIST_ID: {
            type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
            value: distribution.distributionId
          },
          S3_BUCKET: {
            type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
            value: 'barks.devopstar.com'
          }
        }
      },
    });
    buildProject.addToRolePolicy(log_policy);
    buildProject.addToRolePolicy(cloudfront_policy);
    bucket.grantReadWrite(buildProject);

  }
}

import * as cdk from '@aws-cdk/core';
import lambda = require('@aws-cdk/aws-lambda');
import dynamodb = require('@aws-cdk/aws-dynamodb');
import sns = require('@aws-cdk/aws-sns');
import apigw = require('@aws-cdk/aws-apigatewayv2');
import integrations = require('@aws-cdk/aws-apigatewayv2-integrations');

export class BackendStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // ddb
    const table = new dynamodb.Table(this, 'emailsddb', {
      partitionKey: { name: 'email', type: dynamodb.AttributeType.STRING}
    });

    // sns 
    const topic = new sns.Topic(this, 'Topic', {
      displayName: 'Subscription topic',
      
    });

    // lambda
    const fn = new lambda.Function(this, 'lambdafn', {
      runtime: lambda.Runtime.PYTHON_3_8,
      code: lambda.Code.fromAsset('lambda'),
      handler: 'app.signup',
      environment: {
        TABLE_NAME: table.tableName,
        SIGNUP_TOPIC: topic.topicName,
        DEBUG: "true"
      }
    });

    // iam
    table.grantReadWriteData(fn);
    topic.grantPublish(fn);

    // api gw
    let api = new apigw.HttpApi(this, 'api', {
      defaultIntegration: new integrations.LambdaProxyIntegration({
        handler: fn
      })
    });

    // output api gw
    new cdk.CfnOutput(this, 'HTTP API URL', {
      value: api.url ?? 'Something went wrong'
    });
  }
}

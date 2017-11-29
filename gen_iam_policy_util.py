import StringIO


BEGIN_POLICY="""{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "dynamodb:ListTables"
            ],
            "Effect": "Allow",
            "Resource": "*"
        },
"""
TABLE_POLICY = """        {
            "Action": [
                "dynamodb:*"
            ],
            "Effect": "Allow",
            "Resource": [
                "arn:aws:dynamodb:us-west-2:734808183624:table/%s"
            ]
        },
        {
            "Action": [
                "dynamodb:*"
            ],
            "Effect": "Allow",
            "Resource": [
                "arn:aws:dynamodb:us-west-2:734808183624:table/%s/*"
            ]
        }"""
END_POLICY="""    ]
}
"""


def GenerateIAMPolicty(table_name_list, tables_suffix):
  iam_policy_io = StringIO.StringIO()
  iam_policy_io.write(BEGIN_POLICY)
  for i, table_name in enumerate(table_name_list):
    table_with_suffix = '%s%s' % (table_name, tables_suffix)
    iam_policy_io.write(TABLE_POLICY % (table_with_suffix, table_with_suffix), )
    if i < len(table_name_list) - 1:
      iam_policy_io.write(',')
    iam_policy_io.write('\n')
  iam_policy_io.write(END_POLICY)
  iam_policy_str = iam_policy_io.getvalue() 
  iam_policy_io.close()
  return iam_policy_str

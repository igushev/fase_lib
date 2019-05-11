"""Tool which by given database class which with static GetTableNameList() generates  AWS IAM Policy.

python3 tools/generate_iam_policy.py <module_name> <database_class_name> <tables_suffix> <output_filepath>

Example:
python3 tools/generate_iam_policy.py fase_server.fase_database DynamoDBFaseDatabase _prod iam_prod.txt
"""


import os
import sys


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


def GenerateIAMPolicty(module_name, database_class_name, tables_suffix, output_filepath):
  exec('import %s' % module_name)
  module = sys.modules[module_name]
  database_class = getattr(module, database_class_name)
  table_name_list = database_class.GetTableNameList()
  
  with open(output_filepath, 'w') as output_file:
    output_file.write(BEGIN_POLICY)
    for i, table_name in enumerate(table_name_list):
      table_with_suffix = '%s%s' % (table_name, tables_suffix)
      output_file.write(TABLE_POLICY % (table_with_suffix, table_with_suffix), )
      if i < len(table_name_list) - 1:
        output_file.write(',')
      output_file.write('\n')
    output_file.write(END_POLICY)


def main(argv):
  assert len(argv) == 5
  module_name = argv[1]
  database_class_name = argv[2]
  tables_suffix = argv[3]
  output_filepath = argv[4]
  GenerateIAMPolicty(module_name, database_class_name, tables_suffix, output_filepath)


if __name__ == '__main__':
  main(os.sys.argv)

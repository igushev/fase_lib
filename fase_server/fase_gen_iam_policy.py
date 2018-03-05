import os

from server_util import gen_iam_policy_util


def main(argv):
  assert 2 <= len(argv) <= 3
  output_filepath = argv[1]
  tables_suffix = argv[2] if len(argv) == 3 else ''
  table_name_list = ['fase_service', 'fase_screen_prog', 'fase_user']
  iam_policy_str = gen_iam_policy_util.GenerateIAMPolicty(table_name_list, tables_suffix)
  with open(output_filepath, 'w') as output_filepath_file:
    output_filepath_file.write(iam_policy_str)


if __name__ == '__main__':
  main(os.sys.argv)

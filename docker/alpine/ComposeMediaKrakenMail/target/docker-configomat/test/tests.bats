load 'test_helper/bats-support/load'
load 'test_helper/bats-assert/all'

@test "Substitue key value pair with spaces: key = value" {
  export TEST_key_1=new_value_1
  ./configomat.sh TEST_ /tmp/example.conf
  assert_success
  grep "key_1 = new_value_1" /tmp/example.conf 2>&1 > /dev/null
  assert_success
}

@test "Substitue key value pair with spaces: key = (&(objectClass=PostfixBookMailAccount)(|(uniqueIdentifier=%n)(mail=%u)))" {
  export "TEST_key_1=(&(objectClass=PostfixBookMailAccount)(|(uniqueIdentifier=%n)(mail=%u)))"
  ./configomat.sh TEST_ /tmp/example.conf
  assert_success
  grep "key_1 = (\&(objectClass=PostfixBookMailAccount)(\|(uniqueIdentifier=\%n)(mail=\%u)))" /tmp/example.conf 2>&1 > /dev/null
  assert_success
}

@test "Substitue key value pair with spaces: key = *+=/_-%&" {
  export TEST_key_2="*+=/_-%&"
  ./configomat.sh TEST_ /tmp/example.conf
  assert_success
  grep 'key_2 = \*+\=\/\_\-\%\&' /tmp/example.conf 2>&1 > /dev/null
  assert_success
}

@test "Substitue key value pair with spaces: key = " {
  export TEST_key_3="new_value_3"
  ./configomat.sh TEST_ /tmp/example.conf
  assert_success
  grep 'key_3 = new_value_3' /tmp/example.conf 2>&1 > /dev/null
  assert_success
}

@test "Substitue key value pair with spaces: key =value" {
  export TEST_key_4="new_value_4"
  ./configomat.sh TEST_ /tmp/example.conf
  assert_success
  grep 'key_4 = new_value_4' /tmp/example.conf 2>&1 > /dev/null
  assert_success
}

# @test "Substitue key value pair with spaces: key= value" {
#   export TEST_key_5="new_value_5"
#   ./configomat.sh TEST_ /tmp/example.conf
#   assert_success
#   grep 'key_5 = new_value_5' /tmp/example.conf 2>&1 > /dev/null
#   assert_success
# }

# @test "Substitue key value pair without spaces: key=value" {
#   export TEST_key_6="new_value_6"
#   ./configomat.sh TEST_ /tmp/example.conf
#   assert_success
#   grep 'key_6 = new_value_6' /tmp/example.conf 2>&1 > /dev/null
#   assert_success
# }

with open(r'C:\Users\imaja\Documents\ClipYantra\backend\tests\test_storage_adapter.py', 'r') as f:
    lines = f.readlines()

# Fix lines 330-335 (upload URL test)
lines[330] = '        # boto3 uses keyword arguments\n'
lines[331] = "        assert call_args.kwargs['ClientMethod'] == 'put_object'\n"
lines[332] = "        assert call_args.kwargs['Params']['Bucket'] == 'test-bucket'\n"
lines[333] = "        assert call_args.kwargs['Params']['Key'] == storage_key\n"
lines[334] = "        assert call_args.kwargs['ExpiresIn'] == 3600\n"

# Fix lines 348-352 (download URL test)
lines[348] = '        # boto3 uses keyword arguments\n'
lines[349] = "        assert call_args.kwargs['ClientMethod'] == 'get_object'\n"
lines[350] = "        assert call_args.kwargs['Params']['Bucket'] == 'test-bucket'\n"
lines[351] = "        assert call_args.kwargs['Params']['Key'] == storage_key\n"
lines[352] = "        assert call_args.kwargs['ExpiresIn'] == 3600\n"

with open(r'C:\Users\imaja\Documents\ClipYantra\backend\tests\test_storage_adapter.py', 'w') as f:
    f.writelines(lines)

print('Fixed')
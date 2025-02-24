from solcx import compile_standard, install_solc

# 安装指定版本的 Solidity 编译器
install_solc('0.8.0')

# 编译合约
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": open("contracts/SimpleStorage.sol").read()}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "evm.bytecode"]}
            }
        },
    },
    solc_version="0.8.0",
)

# 获取 ABI 和字节码
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]
print (abi)
print (bytecode)
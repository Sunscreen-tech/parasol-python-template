// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.19;

import "sunscreen/src/FHE.sol";

contract Counter {
    bytes public number;
    FHE fhe;

    constructor(uint256 seed) {
        fhe = new FHE();
        number = fhe.encryptUint256(seed);
    }

    function setNumber(bytes calldata encryptedNumber) public {
        number = encryptedNumber;
    }

    function increment() public {
        number = fhe.addUint256EncPlain(fhe.networkPublicKey(), number, 1);
    }

    function getPublicKey() public view returns (bytes memory) {
      return fhe.networkPublicKey();
    }

    function getNumberSecretly(bytes memory publicKey) public view returns (bytes memory) {
        return fhe.reencryptUint256(publicKey, number);
    }
}
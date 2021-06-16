import json
import hashlib
import datetime
from flask import Flask, jsonify


class BlockChain():


	def __init__(self,proof,previous_hash):
		self.chain = []
		#Genesis node
		self.create_block(proof,previous_hash) 


	def create_block(self,proof,previous_hash):
		block = {
			'index':len(self.chain)-1,
			'timestamp': str(datetime.datetime.now()),
			'prev_hash':previous_hash,
			'proof':proof
		}
		self.chain.append(block)
		return block

	def get_last_block(self):
		return self.chain[len(self.chain)-1]

	def proof_of_work(self,previous_proof):
		new_proof = 1
		is_valid = False
		while not is_valid:
			hash_op = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
			if hash_op[:4] == '0000':
				is_valid = True
			else:
				new_proof+=1
		return new_proof


	def hash_of_block(self,block):
		encoded = json.dumps(block,sort_keys=True).encode()
		return hashlib.sha256(encoded).hexdigest()


	#Conditions for chain to be valid
	#4 trailing zeros
	#current prev = prev hash

	def chain_is_valid(self,chain):
		prev_block = chain[0]
		block_index = 1
		while block_index < len(chain):
			block = chain[block_index]
			if block['prev_hash'] != self.hash_of_block(prev_block):
				return False

			hash_op = hashlib.sha256(str(prev_block['proof']**2 - block['proof']**2).encode()).hexdigest()

			if hash_op[:4] != '0000':
				return False

			prev_block = chain[block_index]
			block_index+=1

		return True



	def __str__(self):
		return str(self.chain)

block = BlockChain(1,'0')


app = Flask(__name__)

@app.route('/mine',methods=['GET'])
def mine_block():
	prev_block = block.get_last_block()
	prev_proof = prev_block['proof']
	proof = block.proof_of_work(prev_proof)
	prev_hash = block.hash_of_block(prev_block)
	new_block = block.create_block(proof,prev_hash)
	response = {
		'iters':new_block['proof'],
		 'prev_hash':new_block['prev_hash']
	}
	return jsonify(response),200


@app.route('/all',methods=['GET'])
def get_all_blocks():
	return jsonify(block.chain),200

if __name__ == '__main__':
	app.run(debug=True)




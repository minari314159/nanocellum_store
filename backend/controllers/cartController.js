const Cart = require("../models/cart");

//get all carts
const allCarts = async (req, res) => {
	try {
		const carts = await Cart.find();
		res.status(200).json(carts);
	} catch (error) {
		res.status(500).json(error);
	}
};

//get user cart
const userCart = async (req, res) => {
	try {
		const cart = await Cart.findOne({ user_id: req.params.id });
		res.status(200).json(cart);
	} catch (error) {
		res.status(500).json(error);
	}
};

//create a cart
const createCart = async (req, res) => {
	const newCart = new Cart(req.body);
	try {
		const savedCart = await newCart.save();
		res.status(200).json(savedCart);
	} catch (error) {
		res.status(500).json(error);
	}
};

//update a cart
const updateCart = async (req, res) => {
	try {
		const updatedCart = await Cart.findByIdAndUpdate(
			req.params.id,
			{
				$set: req.body,
			},
			{ new: true }
		);
		res.status(200).json(updatedCart);
	} catch (error) {
		res.status(500).json(error);
	}
};

//delete a cart
const deleteCart = async (req, res) => {
	try {
		await Cart.findByIdAndDelete(req.params.id);
		res.status(200).json("Cart has been deleted...");
	} catch (error) {
		res.status(500).json(error);
	}
};

module.exports = { allCarts, userCart, createCart, updateCart, deleteCart };

/* eslint-disable react/prop-types */
import api from "../api";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

const ProductDetail = () => {
	const { id } = useParams();
	const [product, setProduct] = useState({});

	useEffect(() => {
		const getProduct = () => {
			api
				.get(`/api/products/${id}`)
				.then((res) => res.data)
				.then((data) => {
					console.log(data)
					setProduct(data);
				})
				.catch((err) => alert(err));
		};
		getProduct();
	}, [id]);
	if (!product) {
		return <div>Loading...</div>;
	}

	return (
		<section className="w-[40%] flex flex-col justify-center py-5  bg-primary">
			<h1 className="font-bold text-[2rem]">{product.name}</h1>
			<h1 className="font-semibold italic text-[1rem]">{product.color}</h1>
			<img src={product.images[0].image} alt={product.name} />
			<h3>
				<b>Price:</b> {product.price_with_tax}$
			</h3>
			<p className="p-3">{product.description}</p>
			<button
				onClick={null}
				className="bg-amber-800 rounded-2xl py-2 px-2 hover:bg-amber-700 text-white">
				Add to Cart
			</button>
		</section>
	);
};

export default ProductDetail;

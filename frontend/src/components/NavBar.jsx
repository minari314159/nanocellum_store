import { useEffect, useState } from "react";
import { close, logo, menu, login } from "../assets";
import { navLinks } from "../index";
import { NavLink, Link } from "react-router-dom";
import CartWidget from "./CartWidget";
import api from "../api";

const NavBar = () => {
	const [toggle, setToggle] = useState(false);
	const [active, setActive] = useState(false);
	const [quantity, setQuantity] = useState(1);

	const getOrder = async () => {
		try {
			// Step 1: Create a cart if it doesn't exist
			let cartId = localStorage.getItem("cartId");
			// Step 2: Add item to the cart
			const response = await api.get(`/api/carts/${cartId}/`);

			setQuantity(response.data.total_quantity);
		} catch (error) {
			// Handle error (e.g., show an error message)
			alert("Error getting cart items");
		}
	};
	const handleClick = () => {
		setToggle((prev) => !prev);
	};

	useEffect(() => {
		getOrder();
	}, []);

	return (
		<nav className="flex items-center m-0 py-8 px-8 top-0 z-20  justify-between sm:px-13 bg-transparent">
			<NavLink to="/" className="rounded-lg hover:animate-pulse">
				<img
					src={logo}
					alt="nanocellum logo"
					className="bg-transparent w-auto h-[40px]"
				/>
			</NavLink>

			<div className=" flex flex-1 justify-end items-center gap-2">
				<NavLink to="/order">
					<CartWidget quantity={quantity} />
				</NavLink>
				<NavLink to="/login">
					<img
						src={login}
						alt="Menu"
						className="w-[28px] h-[28px] object-contain"
					/>
				</NavLink>

				<img
					src={toggle ? close : menu}
					alt="Menu"
					className="w-[28px] h-[28px] object-contain"
					onClick={handleClick}
				/>
				<div
					className={`${
						toggle ? "flex" : "hidden"
					} p-6 bg-dimWhite absolute top-20 right-0 mx-4 my2 min-w-[140px] rounded-xl sidebar `}>
					<ul className="list-none flex flex-col justify-end items-center flex-1">
						{navLinks.map((nav, index) => (
							<li
								key={nav.id}
								className={`font-poppins font-light cursor-pointer text-[14px] ${
									index === navLinks.length - 1 ? "mr-0" : "mb-4"
								} ${
									active === nav.title ? "text-secondary" : "text-gray-500"
								} hover:text-secondary`}>
								<Link
									to="/"
									onClick={() => {
										setActive(nav.title);
										window.location.replace(`/#${nav.id}`);
									}}>
									{nav.title}
								</Link>
							</li>
						))}
						<NavLink to="/logout">
							<p className="text-[15px]  mt-2 text-gray-500 p-1 ">Logout </p>
						</NavLink>
					</ul>
				</div>
			</div>
		</nav>
	);
};

export default NavBar;

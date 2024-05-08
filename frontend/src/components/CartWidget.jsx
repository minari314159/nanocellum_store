import {cart} from '../assets'

// eslint-disable-next-line react/prop-types
const CartWidget = ({productsCount}) => {
  return (
		<button className="relative">
      <div className="bg-amber-700 absolute text-white rounded-full shadow-md  w-[20px] h-[20px] text-[11px] opacity-80 flex justify-center items-center -top-1 -right-[8px]">
			<span className=" text-[11px] ">
				{productsCount}
			</span>
      </div>
			<img src={cart} alt="Menu" className="w-[28px] h-[28px] object-contain" />
		</button>
	);
}

export default CartWidget
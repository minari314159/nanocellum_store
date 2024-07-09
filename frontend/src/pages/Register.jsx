import Form from "../components/Form";

const Register = () => {
	return (
		<section className="m-0 p-0 h-screen bg-primary">
			<div className="flex flex-col justify-center items-center w-full">
				<div className="p-[6rem]"></div>
				<Form route="/api/customers/" method="register" />
			</div>
		</section>
	);
};

export default Register;

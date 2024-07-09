import Form from "../components/Form";

const Login = () => {
	return (
		<section className="m-0 p-0 h-screen bg-primary">
			<div className="flex flex-col justify-center items-center w-full">
				<div className="p-[6rem]" />
				<Form route="auth/jwt/create/" method="login" />
			</div>
		</section>
	);
};

export default Login;

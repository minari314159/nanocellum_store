import { createContext, useReducer, useEffect } from "react";
import PropTypes from "prop-types";
import { jwtDecode } from "jwt-decode";
import { authReducer, initialState } from "./authReducer";
import { publicRequest, userRequest } from "../../services/requestMethods";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../../services/constants";

// Create the AuthContext
export const AuthContext = createContext();

// AuthProvider component
export const AuthProvider = ({ children }) => {
	const [user, dispatch] = useReducer(authReducer, initialState);

	// Helper functions
	const login = async (username, password) => {
		dispatch({ type: "SET_LOADING", value: true });
		try {
			const res = await publicRequest.post("auth/jwt/create/", {
				username,
				password,
			});
			localStorage.setItem(ACCESS_TOKEN, res.data.access);
			localStorage.setItem(REFRESH_TOKEN, res.data.refresh);
			dispatch({ type: "LOGIN_SUCCESS" });
			return res;
		} catch (error) {
			dispatch({
				type: "SET_ERROR",
				value: error.response?.data?.detail || "Login failed",
			});
			throw error;
		} finally {
			dispatch({ type: "SET_LOADING", value: false });
		}
	};

	const register = async (email, username, password) => {
		dispatch({ type: "SET_LOADING", value: true });
		try {
			await publicRequest.post("auth/users/", {
				email,
				username,
				password,
			});
			dispatch({ type: "REGISTER_SUCCESS" });
		} catch (error) {
			dispatch({
				type: "SET_ERROR",
				value: error.response?.data?.detail || "Registration failed",
			});
			throw error;
		} finally {
			dispatch({ type: "SET_LOADING", value: false });
		}
	};

	const logout = () => {
		localStorage.removeItem(ACCESS_TOKEN);
		localStorage.removeItem(REFRESH_TOKEN);
		dispatch({ type: "LOGOUT" });
	};

	const getCurrentUser = async () => {
		dispatch({ type: "SET_LOADING", value: true });
		try {
			const res = await userRequest.get("/auth/users/me/");
			dispatch({
				type: "SET_USER_DETAILS",
				username: res.data.username,
				email: res.data.email,
				firstName: res.data.first_name,
				lastName: res.data.last_name,
			});
			return res;
		} catch (error) {
			dispatch({ type: "SET_ERROR", value: "Failed to fetch user details" });
		} finally {
			dispatch({ type: "SET_LOADING", value: false });
		}
	};
	const refreshToken = async () => {
		const refreshToken = localStorage.getItem(REFRESH_TOKEN);
		try {
			const res = await userRequest.post("/api/token/refresh/", {
				refresh: refreshToken,
			});
			if (res.status == 200) {
				localStorage.setItem(ACCESS_TOKEN, res.data.access);
				dispatch({ type: "SET_AUTH", value: true });
			} else {
				dispatch({ type: "SET_ERROR", value: "Failed to refresh token" });
				logout();
			}
		} catch (error) {
			dispatch({ type: "SET_ERROR", value: "Failed to refresh token" });
			logout();
		}
	};

	// Check if the user is already logged in when the app starts
	useEffect(() => {
		const checkAuth = async () => {
			dispatch({ type: "SET_LOADING", value: true });
			const accessToken = localStorage.getItem(ACCESS_TOKEN);
			if (!accessToken) {
				dispatch({ type: "LOGOUT" });
				return;
			}
			try {
				const decoded = jwtDecode(accessToken);
				const tokenExpiration = decoded.exp;
				const now = Date.now() / 1000;
				if (tokenExpiration < now) {
					await refreshToken();
				} else {
					dispatch({ type: "SET_AUTH", value: true });
					getCurrentUser();
				}
			} catch (error) {
				dispatch({ type: "SET_ERROR", value: "Failed to authenticate" });
				logout();
			} finally {
				dispatch({ type: "SET_LOADING", value: false });
			}
		};
		checkAuth();
	}, []);

	// Provide state and actions to children
	const value = { user, login, register, logout, getCurrentUser, dispatch };
	return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

AuthProvider.propTypes = {
	children: PropTypes.node.isRequired,
};

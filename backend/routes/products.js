const express = require("express");
const productController = require("../controllers/productController");
const roleAuth = require("../middleware/roleAuth");

const router = express.Router();

//product routes
router.get("/", productController.getAllProducts);

router.get("/:id", productController.getOneProduct);

router.use(roleAuth);

router.post("/", productController.createProduct);

router.patch("/:id", productController.updateProduct);

router.delete("/:id", productController.deleteProduct);

module.exports = router;

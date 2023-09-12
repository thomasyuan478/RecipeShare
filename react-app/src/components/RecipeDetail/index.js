import { useParams } from "react-router-dom/cjs/react-router-dom.min";
import { useDispatch } from "react-redux";
import { useHistory } from "react-router-dom/cjs/react-router-dom.min";
import { useSelector } from "react-redux";
import { useEffect } from "react";
import { getSingleRecipeThunk } from "../../store/recipe";

export const RecipeDetail = () => {
  const { recipeId } = useParams();
  const dispatch = useDispatch();
  // const history = useHistory();
  // const state = useSelector((state) => state.events);
  // const user = useSelector((state) => state.session.user);
  // const group = useSelector((state) => state.groups.singleGroup);
  // const event = useSelector((state) => state.events.SingleEvent);
  // const images = useSelector((state) => state.events.SingleEvent.EventImages);

  useEffect(() => {
    dispatch(getSingleRecipeThunk(recipeId));
  }, [dispatch]);


  const recipe = useSelector((state) => state.recipes.singleRecipe);

  return (
    <>
      <h1>Hello from details Recipe:{recipeId}</h1>
      <div>
        <img src={recipe.cover_image}></img>
        <div>{recipe.name}</div>
        <div>{recipe.ingredient_list}</div>
        <div>{recipe.description}</div>
        <div>{recipe.instruction}</div>
      </div>
      <div>
        <p></p>
      </div>
      <div>
        <div>Reviews Container</div>
        <button>Add Review</button>
      </div>

    </>
  );
};
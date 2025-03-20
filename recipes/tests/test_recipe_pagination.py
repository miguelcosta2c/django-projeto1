from django.urls import reverse

from .test_recipe_base import RecipeTestBase
from unittest.mock import patch


class RecipePaginationTest(RecipeTestBase):
    @patch('recipes.views.PER_PAGE', new=3)
    def test_recipe_search_pagination(self):
        self.make_recipes_in_batch(9)

        urlsearch = reverse('recipes:search')
        response = self.client.get(f'{urlsearch}?q=title')
        list_recipes = response.context['recipes']
        paginator = list_recipes.paginator
        # Asserting that the page has 3 items
        self.assertEqual(len(list_recipes), 3)
        # Asserting that the paginator has 3 pages
        self.assertEqual(paginator.num_pages, 3)

    @patch('recipes.views.PER_PAGE', new=3)
    def test_recipe_pagination_returns_page_1_if_page_is_not_a_number(self):
        self.make_recipes_in_batch(11)

        urlsearch = reverse('recipes:home')
        response = self.client.get(f'{urlsearch}?page=wrongparameter')
        current_page = response.context['pagination_range']['current_page']

        self.assertEqual(current_page, 1)

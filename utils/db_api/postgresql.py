from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_admins(self):
        sql = """
        CREATE TABLE IF NOT EXISTS admins (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        telegram_id BIGINT NULL UNIQUE,
        otp BIGINT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT NOW()
        );
        """
        return await self.execute(sql, execute=True)

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        fullname VARCHAR(255) NOT NULL,
        telegram_id BIGINT NOT NULL UNIQUE,
        language VARCHAR(255) NOT NULL DEFAULT 'uz',
        region VARCHAR(255) NOT NULL,
        phone_number VARCHAR(255) NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT NOW()
        );
        """
        return await self.execute(sql, execute=True)

    async def create_table_products(self):
        sql = """
        CREATE TABLE IF NOT EXISTS products (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        file_id VARCHAR(255) NOT NULL,
        massa VARCHAR(255) NOT NULL,
        price VARCHAR(255) NOT NULL,
        description VARCHAR(255) NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT NOW()
        );
        """
        return await self.execute(sql, execute=True)

    async def create_users_cart(self):
        sql = """
        CREATE TABLE IF NOT EXISTS users_cart (
        id SERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL,
        product_id BIGINT NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT NOW(),
        ispaid VARCHAR(255) NOT NULL,
        count INT DEFAULT 1,
        FOREIGN KEY (user_id) REFERENCES users (telegram_id),
        FOREIGN KEY (product_id) REFERENCES products (id)
        );
        """
        return await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    """
    ---------------------------------------------ADMINS CONTROLLER--------------------------------------------------------
    """

    async def add_admin(self, telegram_id: int, name: str, otp: int):
        sql = """
                INSERT INTO admins(telegram_id, name, otp) VALUES($1, $2, $3)
                """
        await self.execute(sql, telegram_id, name, otp, execute=True)

    async def select_admin(self, **kwargs):
        sql = """
            SELECT * FROM admins WHERE 
            """
        sql, parameters = self.format_args(sql, kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def delete_admin(self, **kwargs):
        sql = """
            DELETE FROM admins WHERE 
            """
        sql, parameters = self.format_args(sql, kwargs)
        await self.execute(sql, *parameters, execute=True)

    async def update_admin(self, telegram_id: int, action: str, otp: int):
        sql = """
            UPDATE admins SET telegram_id=$1, otp=$2 WHERE otp=$3
            """
        return await self.execute(sql, telegram_id, action, otp, execute=True)

    async def select_all_admins(self):
        sql = """
            SELECT * FROM admins
            """
        return await self.execute(sql, fetch=True)

    """
    ---------------------------------------------USER CONTROLLER--------------------------------------------------------
    """

    async def add_user(self, fullname: str, telegram_id: int, language: str, region: str, phone_number: str):
        sql = """
                INSERT INTO users(fullname, telegram_id, language, region, phone_number) VALUES($1, $2, $3, $4, $5)
                """
        await self.execute(sql, fullname, telegram_id, language, region, phone_number, execute=True)

    async def select_user(self, **kwargs):
        sql = """
            SELECT * FROM users WHERE 
            """
        sql, parameters = self.format_args(sql, kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def delete_user(self, **kwargs):
        sql = """
            DELETE FROM users WHERE 
            """
        sql, parameters = self.format_args(sql, kwargs)
        await self.execute(sql, *parameters, execute=True)

    async def select_all_users(self):
        sql = """
            SELECT * FROM users
            """
        return await self.execute(sql, fetch=True)

    """
    ---------------------------------------------PRODUCT CONTROLLER--------------------------------------------------------
    """

    async def add_product(self, name: str, file_id: str, massa: str, price: str, description: str):
        sql = """
                INSERT INTO products(name, file_id, massa, price, description) VALUES($1, $2, $3, $4, $5)
                """
        await self.execute(sql, name, file_id, massa, price, description, execute=True)

    async def select_product(self, **kwargs):
        sql = """
            SELECT * FROM products WHERE 
            """
        sql, parameters = self.format_args(sql, kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def update_product_price(self, id: int, price: str):
        sql = """
            UPDATE products SET price=$1 WHERE id=$2
            """
        return await self.execute(sql, price, id, execute=True)

    async def update_product_desc(self, id: int, description: str):
        sql = """
            UPDATE products SET description=$1 WHERE id=$2
            """
        return await self.execute(sql, description, id, execute=True)

    async def update_product_photo(self, id: int, file_id: str):
        sql = """
            UPDATE products SET file_id=$1 WHERE id=$2
            """
        return await self.execute(sql, file_id, id, execute=True)

    async def delete_product(self, **kwargs):
        sql = """
            DELETE FROM products WHERE 
            """
        sql, parameters = self.format_args(sql, kwargs)
        await self.execute(sql, *parameters, execute=True)

    async def select_all_products(self):
        sql = """
            SELECT * FROM products
            """
        return await self.execute(sql, fetch=True)

    """
    ---------------------------------------------USERS CART CONTROLLER--------------------------------------------------------
    """

    async def add_to_cart(self, user_id: int, product_id: int, isPaid: bool, count: int):
        sql = """
                INSERT INTO users_cart(user_id, product_id, ispaid, count) VALUES($1, $2, $3, $4)
                """
        await self.execute(sql, user_id, product_id, isPaid, count, execute=True)

    async def select_user_cart(self, **kwargs):
        sql = """
            SELECT * FROM users_cart
            JOIN public.products p ON p.id = users_cart.product_id
            JOIN public.users u ON u.telegram_id = users_cart.user_id
            WHERE
            """
        sql, parameters = self.format_args(sql, kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def update_user_cart(self, user_id: int, product_id: int, isPaid: bool):
        sql = """
            UPDATE users_cart SET ispaid=$1 WHERE user_id=$2 AND product_id=$3
            """
        return await self.execute(sql, isPaid, user_id, product_id, execute=True)

    async def delete_user_cart(self, **kwargs):
        sql = """
            DELETE FROM users_cart WHERE 
            """
        sql, parameters = self.format_args(sql, kwargs)
        await self.execute(sql, *parameters, execute=True)

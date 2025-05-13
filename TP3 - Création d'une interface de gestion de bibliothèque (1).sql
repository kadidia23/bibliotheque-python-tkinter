CREATE DATABASE Library;
USE Library;

CREATE TABLE Authors (
    AuthorID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(255) NOT NULL,
    Country VARCHAR(100)
);

CREATE TABLE Books (
    BookID INT PRIMARY KEY AUTO_INCREMENT,
    Title VARCHAR(255) NOT NULL,
    AuthorID INT,
    PublishedYear INT,
    Genre VARCHAR(100),
    Stock INT,
    FOREIGN KEY (AuthorID) REFERENCES Authors(AuthorID) ON DELETE SET NULL
);

CREATE TABLE Borrowings (
    BorrowingID INT PRIMARY KEY AUTO_INCREMENT,
    BookID INT,
    StudentName VARCHAR(255) NOT NULL,
    BorrowDate DATE,
    ReturnDate DATE,
    FOREIGN KEY (BookID) REFERENCES Books(BookID) ON DELETE CASCADE
);

INSERT INTO Authors (AuthorID, Name, Country) VALUES
(1, 'Harper Lee', 'United States'),
(2, 'George Orwell', 'United Kingdom'),
(3, 'Jane Austen', 'United Kingdom'),
(4, 'F. Scott Fitzgerald', 'United States'),
(5, 'Herman Melville', 'United States'),
(6, 'Leo Tolstoy', 'Russia'),
(7, 'J.D. Salinger', 'United States'),
(8, 'J.R.R. Tolkien', 'United Kingdom'),
(9, 'J.K. Rowling', 'United Kingdom'),
(10, 'Dan Brown', 'United States'),
(11, 'Paulo Coelho', 'Brazil'),
(12, 'Miguel de Cervantes', 'Spain'),
(13, 'Cormac McCarthy', 'United States'),
(14, 'Fyodor Dostoevsky', 'Russia'),
(15, 'Khaled Hosseini', 'Afghanistan'),
(16, 'Victor Hugo', 'France'),
(17, 'Emily Brontë', 'United Kingdom'),
(18, 'Mary Shelley', 'United Kingdom');

INSERT INTO Books (BookID, Title, AuthorID, PublishedYear, Genre, Stock) VALUES
(1, 'To Kill a Mockingbird', 1, 1960, 'Fiction', 5),
(2, '1984', 2, 1949, 'Dystopian', 3),
(3, 'Pride and Prejudice', 3, 1813, 'Romance', 4),
(4, 'The Great Gatsby', 4, 1925, 'Fiction', 2),
(5, 'Moby Dick', 5, 1851, 'Adventure', 6),
(6, 'War and Peace', 6, 1869, 'Historical', 2),
(7, 'The Catcher in the Rye', 7, 1951, 'Fiction', 4),
(8, 'The Hobbit', 8, 1937, 'Fantasy', 3),
(9, 'Harry Potter and the Sorcerer''s Stone', 9, 1997, 'Fantasy', 10),
(10, 'The Da Vinci Code', 10, 2003, 'Thriller', 7),
(11, 'Brave New World', 2, 1932, 'Dystopian', 5),
(12, 'The Alchemist', 11, 1988, 'Philosophical', 4),
(13, 'Don Quixote', 12, 1605, 'Adventure', 3),
(14, 'The Road', 13, 2006, 'Post-apocalyptic', 2),
(15, 'Crime and Punishment', 14, 1866, 'Psychological', 6),
(16, 'The Kite Runner', 15, 2003, 'Fiction', 8),
(17, 'The Lord of the Rings', 8, 1954, 'Fantasy', 9),
(18, 'Les Misérables', 16, 1862, 'Historical', 4),
(19, 'Wuthering Heights', 17, 1847, 'Romance', 3),
(20, 'Frankenstein', 18, 1818, 'Science Fiction', 5);

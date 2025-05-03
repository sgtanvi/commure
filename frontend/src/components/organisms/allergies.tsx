import { useEffect, useState } from "react";
import { User } from "../../App";
import { useNavigate } from "react-router-dom";
interface AllergiesPageProps {
    user: User | null
}

const allergiesPage = ({ user }: AllergiesPageProps) => {

    const navigate = useNavigate();
    useEffect(() => {
        console.log('in allergies page');
        console.log('user', user);
        if (user === null) {
            console.log('navigating to login/signup');
            navigate("/loginsignup");
        }
    }, [user]);


    const [newAllergy, setNewAllergy] = useState<string>("");
    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        const trimmedAllergy = newAllergy.trim();
        if (trimmedAllergy && user) {
            // Check if the allergy already exists (case-insensitive)
            const allergyExists = user.allergies.some(
                allergy => allergy.toLowerCase() === trimmedAllergy.toLowerCase()
            );
            
            if (!allergyExists) {
                // Add the new allergy to user.allergies only
                user.allergies.push(trimmedAllergy);
                // Force a re-render by using the spread operator
                setNewAllergy("");
            } else {
                // Optionally: Provide feedback that the allergy already exists
                alert("This allergy is already in your list");
                setNewAllergy("");
            }
        }
    };
    return (
        <div>
            <h1>Allergies</h1>
            {user?.allergies.map((allergy) => (
                <div key={allergy}>
                    <h2>{allergy}</h2>
                </div>
            ))}
            <form
                onSubmit={handleSubmit}
            >
                <input type="text" placeholder="Allergy" value={newAllergy} onChange={(e) => setNewAllergy(e.target.value)} />
                <button type="submit">Add Allergy</button>
            </form>
        </div>
    )
}

export default allergiesPage;
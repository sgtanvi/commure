import { useEffect, useState } from "react";
import { User } from "../../App";
import { useNavigate } from "react-router-dom";
interface ConditionsPageProps {
    user: User | null
}

const conditionsPage = ({ user }: ConditionsPageProps) => {

    const navigate = useNavigate();
    useEffect(() => {
        console.log('in conditions page');
        if (user === null) {
            console.log('navigating to login/signup');
            navigate("/loginsignup");
        }
    }, [user]);


    const [newCondition, setNewCondition] = useState<string>("");
    const [conditions, setConditions] = useState<string[]>(user?.conditions || []);
    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        const trimmedCondition = newCondition.trim();
        if (trimmedCondition && !conditions.includes(trimmedCondition)) {
            // Create a new array instead of modifying the original
            const updatedConditions = [...conditions, trimmedCondition];
            
            // Update user.conditions by replacing it with the new array
            if (user) {
                user.conditions = [...updatedConditions];
            }
            
            // Update local state
            setConditions(updatedConditions);
            
            // Clear the input field
            setNewCondition("");
        } else if (trimmedCondition && conditions.includes(trimmedCondition)) {
            // Alert the user that the condition already exists
            alert("This condition already exists in your list.");
            setNewCondition("");
        }
    };
    return (
        <div>
            <h1>Conditions</h1>
            {conditions.map((condition) => (
                <div key={condition}>
                    <h2>{condition}</h2>
                </div>
            ))}
            <form
                onSubmit={handleSubmit}
            >
                <input type="text" placeholder="Condition" value={newCondition} onChange={(e) => setNewCondition(e.target.value)} />
                <button type="submit">Add Condition</button>
            </form>
        </div>
    )
}

export default conditionsPage;